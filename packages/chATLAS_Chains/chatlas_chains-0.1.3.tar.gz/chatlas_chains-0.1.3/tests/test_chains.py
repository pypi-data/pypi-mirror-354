"""
Unit tests for basic_retrieval_chain

These**NOTE** These require a running postgres database with a populated vector store.

The fixtures used for the tests are defined in conftest.py and are automatically gathered by pytest
"""

import pytest
from langchain_core.runnables import RunnableSequence
from pydantic import ValidationError

from chATLAS_Chains.chains.basic import basic_retrieval_chain
from chATLAS_Chains.prompt.starters import CHAT_PROMPT_TEMPLATE


def test_basic_retrieval_chain_returns_runnablesequence(populated_vector_store):
    """
    Test the search_runnable function with a populated vector store.
    """

    chain = basic_retrieval_chain(
        prompt=CHAT_PROMPT_TEMPLATE, vectorstore=populated_vector_store, model_name="gpt-4o-mini"
    )

    assert isinstance(chain, RunnableSequence)


@pytest.fixture
def vectorstores_list(populated_vector_store):
    return [populated_vector_store for _ in range(3)]


def test_search_runnable_returns_runnablesequence_with_list_of_vectorstores(vectorstores_list):
    chain = basic_retrieval_chain(prompt=CHAT_PROMPT_TEMPLATE, vectorstore=vectorstores_list, model_name="gpt-4o-mini")
    print(type(chain))
    assert isinstance(chain, RunnableSequence)


def test_search_runnable_error_on_invalid_input():
    with pytest.raises(ValidationError):
        basic_retrieval_chain(prompt=CHAT_PROMPT_TEMPLATE, vectorstore="not a vectorstore", model_name="gpt-4o-mini")


def test_search_runnable_returns_docs_and_answer(populated_vector_store):
    chain = basic_retrieval_chain(
        prompt=CHAT_PROMPT_TEMPLATE, vectorstore=populated_vector_store, model_name="gpt-4o-mini"
    )
    output = chain.invoke("What is the Higgs boson?")

    assert "docs" in output
    assert "answer" in output

    assert isinstance(output["docs"], list)
