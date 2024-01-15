# AWS monthly billing slack bot

Send AWS monthy summary billing in a slack channel via webhook.

## Example of message

This is an example of message send in Slack:

<p align="center">
  <img src="https://raw.githubusercontent.com/brunoxd13/aws-monthly-billing-slack-bot/master/assets/example.png" alt="logo" />
</p>

<br/ >

## Getting Started

### Prerequisites

To perform the project installation you need to have Serverless Application Model Command Line Interface (SAM CLI) installed in your environment, and to use the SAM CLI, you need the following tools:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

## Installing process

### Cloning the project

```bash
git clone https://github.com/brunoxd13/aws-monthly-billing-slack-bot.git

cd aws-monthly-billing-slack-bot
```

### Instaling the project

Install project depencencies:

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
```

or

```bash
sam build
```

### Configure Slack

Create an [incoming webhook](https://www.slack.com/apps/new/A0F7XDUAZ) on slack.

### Deploy

**IMPORTANT:** Remember to be autentichated in your AWS Account using the AWS CLI.

Deploy the project to your AWS account with the following command:

```bash
sam deploy --guided
```

## Author

[Bruno Russi Lautenschlager](https://github.com/brunoxd13)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
