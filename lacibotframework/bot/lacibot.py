from botbuilder.core import TurnContext, PrivateConversationState
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import ChannelAccount

import openai
import os

from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

if os.name == 'posix':
    # Azure-ben a Linuxon nem jó a sqlite3 verziója, ezért pysqlite3-at használunk helyette
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from data_models import ConversationHistory

# OpenAI API kulcs beállítása
openai.api_key = os.getenv("OPENAI_API_KEY")


class LaciBot(TeamsActivityHandler):

    def __init__(self, conversation_state: PrivateConversationState):
        if conversation_state is None:
            raise TypeError(
                "[Lacibot]: Missing parameter. conversation_state is required but None was given"
            )

        # conversation history elérést biztosító property létrehozása
        self.conversation_state = conversation_state
        self.conversation_history_accessor = self.conversation_state.create_property("ConversationHistory")


         # vector store paraméterek
        self.persist_directory = "res/chroma/"
        self.search_type = "mmr"
        self.search_k = 5
        self.search_fetch_k = 8
        self.lambda_mult = 0.6

        # memória
        self.memory_k = 3

        # ChatGPT paraméterek
        temperature = 0.5
        max_tokens = 500
        model_id = "gpt-3.5-turbo"

        self.embedding = OpenAIEmbeddings()

        # Chroma adatbázis létezésének ellenőrzése
        db_file = self.persist_directory + "chroma.sqlite3"
        if os.path.exists(db_file):
            vectordb = self.load_chroma()
        else:
            vectordb = self.create_chroma()

        llm = ChatOpenAI(model_name= model_id, temperature = temperature, max_tokens = max_tokens)

        # Előzményekből kérdés generálása prompt
        template = """A chat előzményekből és a következő inputból alakíts ki egy önmagában is helytálló kérdést, ha az input értelmezéséhez fontos kontextust tartalmaz!
        Ha az input nem kérdés vagy nem kapcsolódik már az előzményekhez, akkor csak add vissza az inputot!

        Chat előzmények:
        {chat_history}
        
        Következő input: {question}
        
        Átalakított kérdés:"""
        question_generator_prompt = PromptTemplate.from_template(template)
        question_generator_chain = LLMChain(
            llm=llm,
            prompt=question_generator_prompt,
            #verbose=True
        )    

        # Kérdésre válaszoló prompt
        qa_template = """A BME VIK szakmai gyakorlat kérdéseire válaszoló chatbot vagy. A kérdésekre magyarul válaszolj!
        Használd az alábbi dokumentumrészleteket forrásként a felhasználó kérdésének megválaszolásához!
        Ha azokból nem tudsz megadni releváns választ, akkor válaszold azt, hogy "Sajnos erre nem tudok válaszolni, kérdezz mást a BME VIK szakmai gyakorlattal kapcsolatban"
        
        DOKUMENTUMRÉSZLETEK:
        {context}
        
        ÚJ INPUT: {question}
        
        Válaszolj a kérdésre!"""
        
        qa_prompt = PromptTemplate.from_template(qa_template)
        llm_chain = LLMChain(
            llm=llm,
            prompt=qa_prompt,
            #verbose=True
        )
        combine_docs_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
              document_variable_name="context",
              #verbose=True
        )

        # chain létrehozása
        self.chain = ConversationalRetrievalChain(
            combine_docs_chain=combine_docs_chain,
            retriever = vectordb.as_retriever(
                searh_type = self.search_type,
                search_kwargs = {
                     "k": self.search_k,
                     "fetch_k": self.search_fetch_k
                     }
            ),
            question_generator=question_generator_chain,
            #verbose=True
        )

    # adatbázist betöltő függvény
    def load_chroma(self):
        print("Loading Chroma from file")
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding)

    # adatokat betöltő és adatbázist létrehozó függvény
    def create_chroma(self):
        print("Creating Chroma")
        from langchain.document_loaders import CSVLoader, DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        # használt erőforrások mappája
        res_folder = "res/"
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
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )
        vectordb.persist()
        return vectordb


    # Minden eseményre lefutó függvény
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # conversation history mentése
        await self.conversation_state.save_changes(turn_context)

    # Üzenetekre reagáló függvény
    async def on_message_activity(self, turn_context: TurnContext):
        try:
            # memória lekérése
            conversation_data = await self.conversation_history_accessor.get(
                turn_context, ConversationHistory
            )

            # ha nincs még memória, akkor létrehozzuk
            if conversation_data.memory is None:
                conversation_data.memory = ConversationBufferWindowMemory(k = self.memory_k, memory_key="chat_history", return_messages=True)

            # válasz generálása és küldése
            answer = await self.get_answer(turn_context.activity.text, conversation_data.memory)
            await turn_context.send_activity(answer)
        except:
            # hiba esetén hibaüzenet küldése
            await turn_context.send_activity("Hiba lépett fel, kérlek próbáld újra egy kis idő múlva!")
    
    # Választ generáló függvény
    async def get_answer(self, message: str, memory: BaseChatMemory) -> str:
        self.chain.memory = memory
        return self.chain({"question": message})["answer"]
