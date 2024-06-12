# lacibot
Szakmai gyakorlat chatbot

2023 ősz Jeges Gábor szakdolgozat, konzulens: Dr. Forstner Bertalan

## Repository struktúrája

- A **docs** mappában találhatók a heti haladásokról készült markdown fájlok, a képek, és a Word fájlok.
- A **lacibotframework** mappában található a Bot Framework SDK-val készült chatbot, amely Azure-be is deployolva van.
- Az **mt5 training** mappa az mT5 modell finomhangolása alatt keletkező fájlokat tartalmazza, azonban a fájlok mérete miatt nem minden fájl lett feltöltve.
- A **notused notebooks**ban a félév közben elavulttá vált vagy zsákutcába vezető notebookok találhatóak.
- A **res** mappában találhatóak a chatbotokhoz használt forrásfájlok, valamint ide is jön létre a chroma adatbázis az első futtatás alatt.
    - Az **in_use** mappában találhatóak a chatbothoz használt forrásfájlok, amiből előállítottuk a chroma adatbázist.
    - A **not_used** mappában találhatóak a chatbothoz nem használt adatfájlok.
- A **testing** mappában a teszteléshez használt fájlok találhatóak, illetve a teszteredmények, és azok grafikonjai találhatóak.
- A **hubert-qa.ipynb** a finomhangolt huBERT chatbothoz tartozó kódot tartalmazza.
- A **lacibot_gradio.py** a Gradio-s felülettel rendelkező chatbotot tartalmazza.
- Az **mt5_finetune.ipynb** az mT5 modell finomhangolásához szükséges kódot tartalmazza.
- Az **openai_and embeddings_tests.ipynb** a GPT-3.5-ös chatbothoz taartozót kódot, valamint az embedinngek teszteléséhez szükséges kódot tartalmazza.
- A **process_data.ipynb** az adatok gyűjtéséhez, megfelelő fájlformátumra alakításához, valamint kérdés-válasz párok generálásához szükséges kódot tartalmazza.

## Telepítés, futtatás

A projektet a git clone paranccsal tudjuk letölteni a saját gépünkre vagy GitHubon a zöld <> gombra nyomva a "Download zip" opciót választva.

```bash
git clone https://github.com/jgbor/lacibot
```

A szkriptek futtatásához Pyton 3.11-re van szükségünk, amit a [Python hivatalos oldaláról](https://www.python.org/downloads/) tudunk letölteni.

Javasolt egy virtuális környezet létrehozása a projekt számára, amit a következő paranccsal tudunk létrehozni:

```bash
python -m venv lacibot-venv
```

A virtuális környezetet a következő paranccsal tudjuk aktiválni:

```bash
lacibot-venv\Scripts\activate.bat
```

A projekt függőségeit a requirements.txt fájlban találjuk, amit a projekt mapáájából kiadva a következő paranccsal tudunk telepíteni:

```bash
pip install -r requirements.txt
```

Az OpenAI-os kódok futtatásához szükségünk van egy OpenAI API kulcsra, amit a [hivatalos oldalról](https://platform.openai.com/api-keys) tudunk igényelni. A kulcsot ezután környezeti változónak kell beállítanunk, amit a következő paranccsal tudunk megtenni:

```bash
setx OPENAI_API_KEY=<API kulcs>
```

Egy másik megoldás, hogy a kódban a következő sornál a saját API kulcsunkra cseréljük az os.getenv("OPENAI_API_KEY") részt:

```python
openai.api_key = os.getenv("OPENAI_API_KEY")
```

### Gradio-s felülettel rendelkező chatbot futtatása

A projekt futtatásához a következő parancsot kell kiadnunk:

```bash
python lacibot_gradio.py
```

A parancssorban megjelenik egy link, amit a böngészőnkben megnyitva tudjuk használni a chatbotot.

### Jupyter notebookok futtatása

Jupyter notebookokat VS Code-dal és ahhoz telepíthető Jupyter bővítménnyel vagy a következő paranccsal tudjuk elindítani parancssorból:

```bash
jupyter notebook
```

Ebben az esetben böngészőnkben megnyílik a Jupyter notebook, ahol a notebookokat ki tudjuk választani és futtatni külön a mezőket.
A pip install-t tartalmazó mezőket nem kell futtatnunk, ha előtte a requirements.txt fájlban található függőségeket telepítettük.

### Bot Framework SDK-val rendelkező chatbot futtatása

Ha csak ezt szeretnénk futtatni elég a lacibotframework mappában lévő requirements.txt fájlban található függőségeket telepíteni.

A projekt futtatásához a következő parancsot kell kiadnunk a lacibotframwork mappából:

```bash
python app.py
```

A chatfelület használatáhaoz a Bot Framweork Emulator nevű alkalmazásra van szükségünk, amit a [Bot Framework hivatalos oldaláról](https://github.com/microsoft/BotFramework-Emulator/releases/tag/v4.14.1) tudunk letölteni.

Az open bot gombra kattintva tudjuk megnyitni a botot, ahol a bot URL mezőbe a következőt kell beírnunk: http://localhost:3978/api/messages majd a Connect gombra kattintva tudunk üzenetet küldeni a chatbotnak.

### Teams chatbot

#### A bot az alábbi linkről, BME-s fiókkal mobilos Teams-en is elérhető: https://tinyurl.com/4xjpmkf6

![](docs/pics/qr_teams.png)