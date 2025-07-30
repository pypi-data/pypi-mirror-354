from unittest.mock import MagicMock, patch

import pytest

from chATLAS_Chains.llm.model_selection import SUPPORTED_CHAT_MODELS, get_chat_model  # Replace with actual path


@pytest.fixture
def mock_env_key(monkeypatch):
    monkeypatch.setenv("CHATLAS_OPENAI_KEY", "fake-api-key")


@pytest.fixture
def mock_model_class():
    """Returns a MagicMock class that returns a mock instance when called."""
    mock_instance = MagicMock(name="MockChatModelInstance")
    mock_class = MagicMock(name="MockChatModelClass", return_value=mock_instance)
    return mock_class


def test_get_chat_model_valid_model_name(mock_env_key, mock_model_class):
    with patch("importlib.import_module") as mock_import_module:
        mock_import_module.return_value = MagicMock(ChatOpenAI=mock_model_class)

        model = get_chat_model("gpt-4")

        mock_import_module.assert_called_with("langchain_openai")
        mock_model_class.assert_called_once_with(model_name="gpt-4", openai_api_key="fake-api-key")
        assert model is mock_model_class.return_value


def test_get_chat_model_unsupported_model_name_defaults(mock_env_key, mock_model_class):
    with patch("importlib.import_module") as mock_import_module:
        mock_import_module.return_value = MagicMock(ChatOpenAI=mock_model_class)

        model = get_chat_model("unknown-model")

        mock_model_class.assert_called_once_with(model_name="gpt-4o-mini", openai_api_key="fake-api-key")
        assert model is mock_model_class.return_value


def test_get_chat_model_missing_env_var(monkeypatch):
    monkeypatch.delenv("CHATLAS_OPENAI_KEY", raising=False)

    with pytest.raises(ValueError, match="CHATLAS_OPENAI_KEY not set in environment"):
        get_chat_model("gpt-3.5-turbo")


def test_get_chat_model_api_key_stripped(monkeypatch, mock_model_class):
    monkeypatch.setenv("CHATLAS_OPENAI_KEY", "  api-key-with-spaces  ")

    with patch("importlib.import_module") as mock_import_module:
        mock_import_module.return_value = MagicMock(ChatOpenAI=mock_model_class)

        get_chat_model("gpt-4")
        mock_model_class.assert_called_once_with(model_name="gpt-4", openai_api_key="api-key-with-spaces")


def test_get_chat_model_import_error(mock_env_key):
    with patch("importlib.import_module", side_effect=ImportError("Module not found")):
        with pytest.raises(ImportError, match="Module not found"):
            get_chat_model("gpt-4")


def test_get_chat_model_attribute_error(mock_env_key):
    mock_library = MagicMock()
    del mock_library.ChatOpenAI  # simulate missing attribute

    with patch("importlib.import_module", return_value=mock_library):
        with pytest.raises(AttributeError):
            get_chat_model("gpt-4")


def test_all_supported_models_resolve(mock_env_key, mock_model_class):
    """Checks that all models in the supported list work correctly."""
    with patch("importlib.import_module") as mock_import_module:
        mock_import_module.return_value = MagicMock(ChatOpenAI=mock_model_class)

        for model_name in SUPPORTED_CHAT_MODELS:
            result = get_chat_model(model_name)
            assert result is mock_model_class.return_value
