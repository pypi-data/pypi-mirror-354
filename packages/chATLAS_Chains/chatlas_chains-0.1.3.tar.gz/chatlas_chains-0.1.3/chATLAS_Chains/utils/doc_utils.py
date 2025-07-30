from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate, format_document

from chATLAS_Chains.prompt.doc_joiners import DEFAULT_DOCUMENT_JOINER


def combine_documents(
    docs: list[Document], document_prompt: str = DEFAULT_DOCUMENT_JOINER, document_separator: str = "\n\n"
):
    """
    Combine a list of documents into a single formatted string.

    :param docs: The list of documents to combine.
    :type docs: list[Document]
    :param document_prompt: The prompt template used to format each document.
                            Defaults to `DEFAULT_DOCUMENT_JOINER`.
    :type document_prompt: str, optional
    :param document_separator: The separator to place between documents in the final string.
                               Defaults to two newlines.
    :type document_separator: str, optional

    :return: A single string containing all formatted documents joined by the separator.
    :rtype: str
    """

    doc_strings = [format_document(doc, PromptTemplate.from_template(document_prompt)) for doc in docs]

    return document_separator.join(doc_strings)
