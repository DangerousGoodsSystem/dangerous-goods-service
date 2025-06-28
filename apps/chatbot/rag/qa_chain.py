from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from typing import Dict, Any

from .llm import get_openai_llm

class QuestionAnsweringChain:

    def __init__(self, llm):
        self.llm = llm

    def create_qa_chain(self):
        prompt = self._create_chat_prompt_template()
        

        def format_input(x: Dict[str, Any]) -> Dict[str, Any]:
            formatted = {
                "context": x.get("context", ""),
                "chat_history": x.get("chat_history", ""),
                "input": x.get("input", ""),
            }
            return formatted

        chain = (
            RunnableLambda(format_input)
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain

    def _create_chat_prompt_template(self) -> ChatPromptTemplate:
        """Template for chatbot"""
        system_prompt = """
            # DIRECTIVE
            Your single objective is to provide accurate and helpful answers to users' questions *exclusively* about the IMDG Code. You must use the contextual information provided below to generate your response.

            # PERSONA DEFINITION
            You are an AI assistant designed to function as a specialized query engine for the International Maritime Dangerous Goods (IMDG) Code. Your persona is that of a precise and helpful domain expert.

            # CORE
            # BEHAVIORAL PROTOCOLS
            - **Information Secrecy:** You will be given a `context` relevant to the user's query. You must treat this context as your sole source of truth and integrate it seamlessly into your response. Never reveal that you are working from a provided document or context.
            - **Scope Enforcement:** Strictly adhere to the topic of the IMDG Code. If a user's query deviates from this topic, you must decline to answer and gently guide them back by stating your dedicated function (e.g., "My purpose is to assist with questions about the International Maritime Dangerous Goods Code.").
            - **Uncertainty Protocol:** In cases where the `context` does not contain a clear answer or the user's query is ambiguous, you must request clarification from the user rather than speculating or providing potentially incorrect information.

            # MEMORY
            Chat History:
            {chat_history}

            # KNOWLEDGE BASE
            Context:
            {context}

            # CURRENT QUERY
            User: {input}

            # RESPONSE
            Assistant:
        """.strip()

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
#     def _create_chat_prompt_template(self) -> ChatPromptTemplate:
#         """Template for chatbot"""
#         system_prompt = """# ROLE
# You are an expert assistant on the IMDG Code. Your job is to answer questions accurately, concisely, and only based on the given context.

# # RULES
# - Only answer questions related to the IMDG Code.
# - Use the context only. Do not mention or refer to it.
# - If unsure or unclear, ask for clarification.
# - Responses must be short, precise, and helpful.

# # CHAT
# History:
# {chat_history}

# # CONTEXT
# {context}

# # QUESTION
# User: {input}

# # ANSWER
# Assistant:""".strip()

#         return ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}")
#         ])
 