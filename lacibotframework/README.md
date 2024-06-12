# Microsoft Lacibot Framework

## BME VIK szakmai gyakorlat chatbot


### Projekt felépítése

- **Bot** mappa: Az általam írt LangChain-es chatbotból átalakított Bot Framework-ös bot található itt.
- **Data_models**: A chat előzményekhez szükséges adatmodell, a ConversationHistory osztály található itt.
- **Res** mappa: a bot által használt források.
- DeploymentTemplates: Azure deployment sablonok.
- **app.py**: A bot futtatásához szükséges fő fájl, ez indítja el a szervert.
- **config.py**: A bot konfigurációs fájlja. A portot, a MicrosoftAppID-t és a MicrosoftAppPassword-öt tartalmazza.

Az alábbi eredeti sablonból átvett leírással lehet tesztelni a botot lokálisan:

This bot has been created using [Bot Framework](https://dev.botframework.com).

## Prerequisites

This sample **requires** prerequisites in order to run.

### Install Python 3.11

## Running the sample
- Run `pip install -r requirements.txt` to install all dependencies
- Run `python app.py`


## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- Enter a Bot URL of `http://localhost:3978/api/messages`