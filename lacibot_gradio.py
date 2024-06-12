import os
import openai

if os.name == 'posix':
    # Azure-ben a Linuxon nem jó a sqlite3 verziója, ezért pysqlite3-at használunk helyette
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

import gradio as gr

# OpenAI API kulcs beállítása
openai.api_key = os.getenv("OPENAI_API_KEY")

# vector store paraméterek
persist_directory = "res/chroma/"
search_type = "mmr"
search_k = 5
search_fetch_k = 8
lambda_mult = 0.6

# memória
memory_k = 3

# ChatGPT paraméterek
temperature = 0.5
max_tokens = 500
model_id = "gpt-3.5-turbo"

embedding = OpenAIEmbeddings()

# adatbázist betöltő függvény
def load_chroma():
    print("Loading Chroma from file")
    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

# adatokat betöltő és adatbázist létrehozó függvény
def create_chroma():
    print("Creating Chroma")
    from langchain.document_loaders import CSVLoader, DirectoryLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # használt erőforrások mappája
    res_folder = "res/in_use/"
    # splitting paraméterek
    chunk_size = 500
    chunk_overlap = 50

    # erőforrások betöltése
    directory_loader = DirectoryLoader(res_folder, glob="*.csv", use_multithreading=True, loader_cls=CSVLoader, loader_kwargs={"encoding": "utf-8"})
    csv_data = directory_loader.load()
    directory_loader = DirectoryLoader(res_folder, glob="*.txt", use_multithreading=True, loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    text_data = directory_loader.load()

    # szöveges erőforrások felbontása
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=True,
        separators=["\n\s*\n", "\n\s*", "\n"]
    )
    split_text_data = text_splitter.split_documents(text_data)
    combined_data = []
    combined_data.extend(split_text_data)
    combined_data.extend(csv_data)

    # Chroma létrehozása a dokumentumokból
    vectordb = Chroma.from_documents(
        documents=combined_data,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb


# Chroma adatbázis létezésének ellenőrzése
db_file = persist_directory + "chroma.sqlite3"
if os.path.exists(db_file):
    vectordb = load_chroma()
else:
    vectordb = create_chroma()


memory = ConversationBufferWindowMemory(k = memory_k, memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(model_name= model_id, temperature = temperature, max_tokens = max_tokens)

# Előzményekből kérdés generálása prompt
template = """A chat előzményekből és a következő inputból alakíts ki egy önmagában is helytálló kérdést, ha az input értelmezéséhez fontos kontextust tartalmaz!
Ha az input nem kérdés vagy nem kapcsolódik már az előzményekhez, akkor csak add vissza az inputot!

Chat előzmények:
{chat_history}

Következő input: {question}

Átalakított kérdés:"""
question_generator_prompt = PromptTemplate.from_template(template)
question_generator_chain = LLMChain(llm=llm, prompt=question_generator_prompt)

# Kérdésre válaszoló prompt
qa_template = """A BME VIK szakmai gyakorlat kérdéseire válaszoló chatbot vagy. A kérdésekre magyarul válaszolj!
Használd az alábbi dokumentumrészleteket forrásként a felhasználó kérdésének megválaszolásához!
Ha azokból nem tudsz megadni releváns választ, akkor válaszold azt, hogy "Sajnos erre nem tudok válaszolni, kérdezz mást a BME VIK szakmai gyakorlattal kapcsolatban"

DOKUMENTUMRÉSZLETEK:
{context}

ÚJ INPUT: {question}

Válaszolj a kérdésre!"""

qa_prompt = PromptTemplate.from_template(qa_template)
llm_chain = LLMChain(llm=llm, prompt=qa_prompt)
combine_docs_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")

# chain létrehozása
chain = ConversationalRetrievalChain(
    combine_docs_chain=combine_docs_chain,
    retriever = vectordb.as_retriever(
        searh_type = search_type,
        search_kwargs = {
             "k": search_k,
             "fetch_k": search_fetch_k
             }
    ),
    question_generator=question_generator_chain,
    memory=memory
)

# gradio chat UI létrehozása és indítása
def qa(message, history) -> str:
    yield chain({"question": message})["answer"]
    
chat_ui = gr.ChatInterface(qa, title = "Lacibot", description="Kérdezz a VIK-es szakmai gyakorlatról!", undo_btn=None)
chat_ui.queue().launch()   