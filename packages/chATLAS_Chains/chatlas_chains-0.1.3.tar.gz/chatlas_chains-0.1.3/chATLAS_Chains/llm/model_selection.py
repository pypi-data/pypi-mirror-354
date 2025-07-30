import importlib
import os

SUPPORTED_CHAT_MODELS = {
    "gpt-3.5-turbo": {"library": "langchain_openai", "module": "ChatOpenAI"},
    "gpt-4": {"library": "langchain_openai", "module": "ChatOpenAI"},
    "gpt-4o": {"library": "langchain_openai", "module": "ChatOpenAI"},
    "gpt-4o-mini": {"library": "langchain_openai", "module": "ChatOpenAI"},
}


def get_chat_model(model_name):
    """
    Initialize chat model with the provided model name (if supported)

    This function dynamically imports the appropriate library and model class based on
    the given `model_name`, initializes it using the `CHATLAS_OPENAI_KEY` from the environment,
    and returns the model instance. If the model name is not supported, it defaults to `"gpt-4o-mini"`.

    :param model_name: The name of the model to load (e.g., "gpt-4", "gpt-3.5-turbo").
    :type model_name: str

    :raises ValueError: If the environment variable `CHATLAS_OPENAI_KEY` is not set.

    :return: An instance of the specified chat model.
    :rtype: BaseLanguageModel
    """

    if model_name not in SUPPORTED_CHAT_MODELS:
        model_name = "gpt-4o-mini"

    api_key = os.getenv("CHATLAS_OPENAI_KEY")
    if not api_key:
        raise ValueError("CHATLAS_OPENAI_KEY not set in environment")
    api_key = api_key.strip()

    model_config = SUPPORTED_CHAT_MODELS[model_name]
    library = model_config["library"]
    module = model_config["module"]

    library = importlib.import_module(library)
    model_class = getattr(library, module)

    # Dynamically create the model instance
    model = model_class(model_name=model_name, openai_api_key=api_key)

    return model
