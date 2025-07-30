"""
Example graph for running langgraph with this general setup and the postgres vector stores.
"""

from typing import TypedDict

import langgraph.graph as lg
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph

from chATLAS_Chains.llm.model_selection import get_chat_model
from chATLAS_Chains.utils.doc_utils import combine_documents
from chATLAS_Embed import LangChainVectorStore


# Define TypedDict for the state
class GraphState(TypedDict, total=False):
    question: str
    search_kwargs: dict
    retrieved_docs: dict[str, list[Document]]
    merged_docs: list[Document]
    context: str
    answer: str


def basic_retrieval_graph(prompt: str, vectorstore, model_name: str) -> lg.Graph:
    """
    Baseline RAG retrieval graph using LangGraph. Searches one or several vectorstores,
    passes retrieved documents to the model, and returns the final answer.

    Args:
        prompt: str, the prompt to use for the model
        vectorstore: the vectorstore(s) to search
        model_name: str, the name of the model to use for the response

    Returns:
        A LangGraph graph that can be executed for RAG
    """
    # Initialize the model and prompt template
    model = get_chat_model(model_name)
    prompt_template = ChatPromptTemplate.from_template(prompt)

    # Create a list of retrievers from the vectorstore(s)
    if isinstance(vectorstore, list):
        retrievers = [LangChainVectorStore(vector_store=vs) for vs in vectorstore]
    else:
        retrievers = [LangChainVectorStore(vector_store=vectorstore)]

    # Define the retrieval function
    def retrieve_documents(state: GraphState) -> GraphState:
        """Retrieve documents from all vectorstores."""
        question = state["question"]
        search_kwargs = state.get("search_kwargs", {})  # Get search params from state
        docs_dict = {}

        for i, retriever in enumerate(retrievers):
            docs_dict[f"docs_{i}"] = retriever.invoke(
                question,
                config={"metadata": {"search_kwargs": search_kwargs}},  # Pass search params to retriever
            )

        return {
            "question": question,
            "search_kwargs": search_kwargs,
            "retrieved_docs": docs_dict,
        }

    # Define the document merging function
    def merge_docs(state: GraphState) -> GraphState:
        """Merge all retrieved documents into a single list."""
        docs_dict = state["retrieved_docs"]
        all_docs = []

        for i in range(len(retrievers)):
            all_docs.extend(docs_dict[f"docs_{i}"])

        return {
            "question": state["question"],
            "retrieved_docs": state["retrieved_docs"],
            "merged_docs": all_docs,
        }

    # Define the document processing function
    def process_docs(state: GraphState) -> GraphState:
        """Process the merged documents into a context string."""
        docs = state["merged_docs"]
        context = combine_documents(docs)
        return {
            "question": state["question"],
            "retrieved_docs": state["retrieved_docs"],
            "merged_docs": state["merged_docs"],
            "context": context,
        }

    # Define the answer generation function
    def generate_answer(state: GraphState) -> GraphState:
        """Generate an answer using the LLM."""
        question = state["question"]
        context = state["context"]

        prompt_input = {"context": context, "question": question}

        chain = prompt_template | model
        response = chain.invoke(prompt_input)
        answer = response.content

        return {
            "question": state["question"],
            "retrieved_docs": state["retrieved_docs"],
            "merged_docs": state["merged_docs"],
            "context": state["context"],
            "answer": answer,
        }

    # Build the graph with the defined state schema
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("retrieve", retrieve_documents)
    graph.add_node("merge", merge_docs)
    graph.add_node("process", process_docs)
    graph.add_node("generate", generate_answer)

    # Define the edges
    graph.add_edge("retrieve", "merge")
    graph.add_edge("merge", "process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)

    # Set the entry point
    graph.set_entry_point("retrieve")

    # Compile the graph
    return graph.compile()


if __name__ == "__main__":
    # Example of how to run the graph correctly
    import os

    os.environ["CHATLAS_EMBEDDING_MODEL_PATH"] = "<PATH TO YOUR EMBEDDING MODEL>"
    os.environ["CHATLAS_OPENAI_KEY"] = "YOUR OPENAI API KEY"
    os.environ["CHATLAS_DB_PASSWORD"] = "<>"

    from ..prompt.starters import CHAT_PROMPT_TEMPLATE
    from ..vectorstore import vectorstore

    graph = basic_retrieval_graph(prompt=CHAT_PROMPT_TEMPLATE, vectorstore=vectorstore, model_name="gpt-4o-mini")

    ans = graph.invoke(
        {
            "question": "How many onions are in ATLAS",
            "search_kwargs": {
                "k_text": 3,
                "k": 10,
                "date_filter": "01-01-2010",
                "type": ["CDS", "twiki", "Indico"],
            },
        }
    )

    print(ans)
