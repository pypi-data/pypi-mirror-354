from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough, RunnableSequence

from chATLAS_Embed.Base import VectorStore
from chATLAS_Embed.LangChainVectorStore import LangChainVectorStore


def search_runnable(
    vectorstore: VectorStore | list[VectorStore],
) -> RunnableSequence:
    """
    LangChain RunnableSequence to search one or more vectorstores in parallel.

    :param vectorstore: A single `VectorStore` or a list of `VectorStore` instances
    :type vectorstore: VectorStore or list[VectorStore]

    :return: A LangChain `RunnableSequence` that performs retrieval. Results from multiple vectorstores are merged into a single list.
    :rtype: RunnableSequence
    """

    # Create a list of retrievers from each vectorstore
    if isinstance(vectorstore, list):
        retrievers = [LangChainVectorStore(vector_store=vs) for vs in vectorstore]
    else:
        retrievers = [LangChainVectorStore(vector_store=vectorstore)]

    # Create parallel retrieval for each retriever
    retrieved_documents = RunnableParallel(
        {f"docs_{i}": retriever for i, retriever in enumerate(retrievers)} | {"question": RunnablePassthrough()}
    )

    # Merge all retrieved documents into a single list
    def merge_docs(x):
        all_docs = []
        for i in range(len(retrievers)):
            all_docs.extend(x[f"docs_{i}"])
        return all_docs

    # take the retrived docs and merge them, also pass through the question
    processed = RunnableParallel(
        {"docs": RunnableLambda(merge_docs), "question": RunnableLambda(lambda x: x["question"])}
    )

    searcher = retrieved_documents | processed

    return searcher
