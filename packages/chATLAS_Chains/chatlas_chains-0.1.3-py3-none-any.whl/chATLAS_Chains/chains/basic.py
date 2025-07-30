from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from chATLAS_Chains.llm.model_selection import get_chat_model
from chATLAS_Chains.search.basic import search_runnable
from chATLAS_Chains.utils.doc_utils import combine_documents


def basic_retrieval_chain(prompt: str, vectorstore, model_name: str) -> RunnableParallel:
    """
    Baseline RAG retrieval chain. Searches one or several vectorstores in parallel, passes retrieved documents to the model

    :param prompt: The prompt template to use with the model.
    :type prompt: str
    :param vectorstore: The vectorstore or list of vectorstores to search over.
    :type vectorstore: Any
    :param model_name: The name of the chat model to use for generating responses.
    :type model_name: str

    :return: A LangChain RunnableParallel chain that performs retrieval and response generation.
    :rtype: RunnableParallel

    """
    prompt = ChatPromptTemplate.from_template(prompt)
    model = get_chat_model(model_name)

    search = search_runnable(vectorstore)

    final_inputs = {
        "context": lambda x: combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    answer = {
        "answer": final_inputs | prompt | model,
        "docs": lambda x: x["docs"],
    }

    chain = search | answer
    return chain
