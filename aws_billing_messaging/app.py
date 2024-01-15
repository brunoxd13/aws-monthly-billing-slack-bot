from collections import defaultdict

import http.client
import calendar
import datetime
import boto3
import json
import os


low_cost = int(os.getenv("LOW_COST"))
high_cost = int(os.getenv("HIGH_COST"))


TELEGRAM_API_HOST = "api.telegram.org"
SLACK_API_URL = "hooks.slack.com"

def lambda_handler(_event, _context):
    report_cost = get_report_cost()
    
    send_slack_message(report_cost)
    send_telegram_message(report_cost)
    
    
def get_report_cost():
    client = boto3.client('ce')
    
    last_month_day = calendar.monthrange(
        datetime.date.today().year, datetime.date.today().month)[1]

    start_date = datetime.date.today().replace(day=1)
    end_date = datetime.date.today().replace(day=last_month_day)
    
    query = {
        "TimePeriod": {
            "Start": start_date.strftime('%Y-%m-%d'),
            "End": end_date.strftime('%Y-%m-%d'),
        },
        "Granularity": "MONTHLY",
        "Filter": {
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": [
                        "Credit",
                        "Refund",
                        "Upfront",
                        "Support",
                    ]
                }
            }
        },
        "Metrics": ["UnblendedCost"],
        "GroupBy": [
            {
                "Type": "DIMENSION",
                "Key": "SERVICE",
            },
        ],
    }

    result = client.get_cost_and_usage(**query)

    buffer = "%-40s %5s\n" % ("Services", "Budget")

    cost_by_service = defaultdict(list)

    # Build a map of service -> array of daily costs for the time frame
    for day in result['ResultsByTime']:
        for group in day['Groups']:
            key = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])

            cost_by_service[key].append(cost)

    most_expensive_services = sorted(
        cost_by_service.items(), key=lambda i: i[1][-1], reverse=True)
    
    service_quantity = int(os.getenv("SERVICE_QUANTITY"))
    
    if len(most_expensive_services) < service_quantity:
        service_quantity = len(most_expensive_services)
    
    for service_name, costs in most_expensive_services[:service_quantity]:
        buffer += "%-40s US$ %5.2f\n" % (service_name, costs[-1])

    other_costs = 0.0
    for service_name, costs in most_expensive_services[service_quantity:]:
        for i, cost in enumerate(costs):
            other_costs += cost

    buffer += "%-40s US$ %5.2f\n" % ("Other", other_costs)

    total_costs = 0.0
    for service_name, costs in most_expensive_services:
        for i, cost in enumerate(costs):
            total_costs += cost

    buffer += "%-40s US$ %5.2f\n" % ("Total", total_costs)

    if total_costs < low_cost:
        emoji = "💰"
    elif total_costs > high_cost:
        emoji = "😱 ATTENTION the billing is very high ❗❗❗\n"
    else:
        emoji = "🙉 ATTENTION billing is at a worrying level ⚠\n"

    summary = "%s Current billing is at: US$ *%5.2f*" % (emoji, total_costs)
    
    
    text = summary + "\n\n```\n" + buffer + "```"
    
    return text
    
    
def send_telegram_message(message):
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    conn = http.client.HTTPSConnection(TELEGRAM_API_HOST)
    
    if telegram_token is not None or telegram_chat_id is not None:

        endpoint = f"/bot{telegram_token}/sendMessage"

        payload = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        headers = {"content-type": "application/json"}

        conn.request("POST", endpoint, json.dumps(payload), headers)

        res = conn.getresponse()

        return {
            "statusCode": res.status,
            "body": json.dumps("Lambda executed.")
        }
    else:
        raise EnvironmentError("Missing TELEGRAM_TOKEN, TELEGRAM_CHAT_ID env variable!")
        

def send_slack_message(message):
    slack_token = os.environ.get('SLACK_WEBHOOK_TOKEN')
    
    if slack_token is not None:
        conn = http.client.HTTPSConnection(SLACK_API_URL)
        
        endpoint = f"/services/{slack_token}"
        
        payload = { "text": message }

        headers = { "content-type": "application/json" }

        conn.request("POST", endpoint, json.dumps(payload), headers)

        res = conn.getresponse()

        return {
            "statusCode": res.status,
            "body": json.dumps("Lambda executed.")
        }
    else:
        raise EnvironmentError("Missing SLACK_WEBHOOK_TOKEN env variable!")
        
    