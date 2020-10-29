# AWS monthly billing slack bot

Send AWS monthy summary billing in a slack channel via webhook.


## Example of message
This is an example of message send in Slack:

<p align="center">
  <img src="https://raw.githubusercontent.com/brunoxd13/aws-monthly-billing-slack-bot/master/assets/example.png" alt="logo" />
</p>
<br>

## Getting Started

### Prerequisites

To perform the project installation you need to have a package manager installed in your environment, such as the following:
* [Yarn](https://yarnpkg.com/pt-BR/)
* [Npm](https://www.npmjs.com)

## Installing process
### Cloning the project
```
git clone https://github.com/brunoxd13/aws-monthly-billing-slack-bot.git

cd aws-monthly-billing-slack-bot
```

###  Instaling the project
Install project depencencies:

`npm install`

### Create `.env` file

Define environment variables to work correctly, eg.:

```
SERVICE_QUANTITY=5
LOW_COST=70
HIGH_COST=100
```

Or just rename file `.env-example` to `.env`.

### Configure Slack

Create an [incoming webhook](https://www.slack.com/apps/new/A0F7XDUAZ) on slack.

### Deploy
**IMPORTANT:** Configure the [serverless file](./serverless.yml) whith with your provider credentials. You can use this [guide](https://www.serverless.com/framework/docs/providers/aws/guide/credentials#create-an-iam-user-and-access-key). 

Deploy the project to your AWS account with the following command:

`npm run deploy -- --slack_url="<slack_webhook_url>"`

## Author
[Bruno Russi Lautenschlager](https://github.com/brunoxd13)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details