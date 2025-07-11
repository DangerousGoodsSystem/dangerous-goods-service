from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever

context_prompt = """
Given the conversation history and the user's latest question, rewrite the question to be self-contained so that it can be understood without referring to the previous conversation context.

Do not answer the question.

Only rewrite the question if necessary to make it self-contained. If the question is already self-contained, return it unchanged.
"""

class ContextualRetriever:
    def __init__(self, llm, retriever):        
        self.llm = llm
        self.retriever = retriever

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", context_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

    def get_history_aware_retriever(self):
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            self.retriever, 
            self.prompt_template
        )
        return history_aware_retriever