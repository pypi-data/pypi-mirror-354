"""
Unit tests for search_runnable

**NOTE** These require a running postgres database with a populated vector store.

The fixtures used for the tests are defined in conftest.py and are automatically gathered by pytest

"""

import pytest
from langchain_core.runnables import RunnableSequence
from pydantic import ValidationError

from chATLAS_Chains.search.basic import search_runnable


def test_search_runnable_returns_runnablesequence(populated_vector_store):
    """
    Test the search_runnable function with a populated vector store.
    """
    print(type(populated_vector_store))
    # Create a runnable for searching
    searcher = search_runnable(vectorstore=populated_vector_store)

    assert isinstance(searcher, RunnableSequence)


@pytest.fixture
def vectorstores_list(populated_vector_store):
    return [populated_vector_store for _ in range(3)]


def test_search_runnable_returns_runnablesequence_with_list_of_vectorstores(vectorstores_list):
    runnable = search_runnable(vectorstores_list)
    assert isinstance(runnable, RunnableSequence)


def test_search_runnable_error_on_invalid_input():
    with pytest.raises(ValidationError):
        search_runnable("not_a_vectorstore")


def test_search_runnable_returns_docs_and_questions(populated_vector_store):
    searcher = search_runnable(vectorstore=populated_vector_store)
    output = searcher.invoke("What is the Higgs boson?")

    assert "docs" in output
    assert "question" in output
