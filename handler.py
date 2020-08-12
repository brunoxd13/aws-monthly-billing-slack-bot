from collections import defaultdict
import boto3
import datetime
import os
import requests
import sys

start_date = datetime.date.today().replace(day=1)
end_date = datetime.date.today()

def report_cost(event, context):
    client = boto3.client('ce')

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

    most_expensive_services = sorted(cost_by_service.items(), key=lambda i: i[1][-1], reverse=True)

    for service_name, costs in most_expensive_services[:5]:
        buffer += "%-40s US$ %5.2f\n" % (service_name, costs[-1])

    other_costs = 0.0
    for service_name, costs in most_expensive_services[5:]:
        for i, cost in enumerate(costs):
            other_costs += cost

    buffer += "%-40s US$ %5.2f\n" % ("Other", other_costs)

    total_costs = 0.0
    for service_name, costs in most_expensive_services:
        for i, cost in enumerate(costs):
            total_costs += cost

    buffer += "%-40s US$ %5.2f\n" % ("Total", total_costs)

    if total_costs < 70:
        emoji = ":spinner:"
    elif total_costs > 100:
        emoji = ":scream: ATENÇÃO @here o billing está muito alto :redsiren: \n"
    else:
        emoji = ":zany_face: ATENÇÃO @here o billing está em um nível preocupante :warning: \n"

    summary = "%s Billing atual está em: US$ %5.2f" % (emoji, total_costs)

    hook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if hook_url:
        resp = requests.post(
            hook_url,
            json={
                "text": summary + "\n\n```\n" + buffer + "```",
            }
        )

        if resp.status_code != 200:
            print("HTTP %s: %s" % (resp.status_code, resp.text))
    else:
        print(summary)
        print(buffer)
