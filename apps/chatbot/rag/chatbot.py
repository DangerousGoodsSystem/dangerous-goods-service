from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain.chains import create_retrieval_chain
from .llm import get_openai_llm, get_local_llm
from .vector_db import VectorDB
from .contextual_retriever import ContextualRetriever
from .qa_chain import QuestionAnsweringChain
from .state_manager import StateManager
from .standardize import preprocess_text
import os

class Chatbot:
    def __init__(self):
        self.llm = get_openai_llm()
        self.local_llm = get_local_llm()
        
        self.vector_db = VectorDB() 
        
        # Khởi tạo bộ nhớ
        self.memory = MemorySaver()
        
        self.retriever = None
        self.contextual_retriever = None
        self.qa_chain = None
        self.rag_chain = None
        
        if self._has_vector_data():
            self._initialize_retrieval()

    def _has_vector_data(self):
        vector_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector_store/indexes")
        index_faiss = os.path.join(vector_db_path, "index.faiss")
        index_pkl = os.path.join(vector_db_path, "index.pkl")
        
        return (os.path.exists(index_faiss) and os.path.getsize(index_faiss) > 0 and
                os.path.exists(index_pkl) and os.path.getsize(index_pkl) > 0)

    def _initialize_retrieval(self):
        self.retriever = self.vector_db.get_retriever()
        self.contextual_retriever = ContextualRetriever(self.llm, self.retriever).get_history_aware_retriever()
        self.qa_chain = QuestionAnsweringChain(self.local_llm).create_qa_chain()
        self.rag_chain = create_retrieval_chain(self.contextual_retriever, self.qa_chain)

    def is_retrieval_ready(self):
        return self.rag_chain is not None


    def call_model(self, state: StateManager):
        question = preprocess_text(state["input"])
        if self.is_retrieval_ready():
            response = self.rag_chain.invoke(state)
            return {
                "chat_history": [
                    HumanMessage(question),
                    AIMessage(response["answer"]),
                ],
                "context": response["context"],
                "answer": response["answer"],
            }
        else:
            # chưa test case này
            response = self.local_llm.invoke(question)
            answer = response.content if hasattr(response, 'content') else str(response)
            return {
                "chat_history": [
                    HumanMessage(question),
                    AIMessage(answer),
                ],
                "context": [],
                "answer": answer,
            }
        
    def setup_workflow(self):        
        self.workflow = StateGraph(state_schema=StateManager)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)
        self.app = self.workflow.compile(checkpointer=self.memory)
        return self.app


    def ask(self, question: str, config: dict):
        
        state = {
            "input": question,
            "chat_history": [],
            "context": "",
            "answer": "",
        }
        
        result = self.app.invoke(state, config=config)
        # pretty_print_docs(result["context"])
        
        return {"answer": result["answer"], "documents": result["context"]}