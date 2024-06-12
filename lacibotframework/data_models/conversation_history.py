from langchain.memory.chat_memory import BaseChatMemory

# Beszélgetés memóriáját tároló osztály
class ConversationHistory:
    def __init__(
            self,
            memory: BaseChatMemory = None,
    ):
        self.memory = memory