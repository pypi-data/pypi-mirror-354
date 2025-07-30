
# chATLAS_Chains

This package implements and benchmarks various Retrieval Augmented Generation (RAG) chains for use in the [chATLAS](https://chatlas-flask-chatlas.app.cern.ch) project.

## Installation

```bash
conda create -n venv chatlas_chains_env python=3.10
conda activate chatlas_chains_env
pip install chatlas-chains
```

## Environment variables

These are required for the following use cases

1. Using an OpenAI LLM
```bash
export CHATLAS_OPENAI_KEY='your api key'
```

2. Benchmarking, set the path to the question set
```bash
export CHATLAS_BENCHMARK_QUESTIONS=/path/to/questions.josn
```

## Available Chains
- chains.basic.basic_retrieval_chain
- chains.basic_graph.basic_retrieval_graph

## Benchmarking

To benchmark e.g. the chains in `chATLAS_Chains.chains.basic` run this from the project root
```bash
python benchmark/basic.py
```

## Testing

The tests require a running postgres server to work. If on lxplus you can modify `TEST_DB_CONFIG` in [tests/conftest.py](tests/conftest.py) to connect to the chATLAS server.

If you want to create a local dummy postgres server, you need to install `psql`. This can be done on macOS using [homebrew](https://brew.sh):

Software install
```bash
brew install postgresql
brew services start postgresql
brew install pgvector
brew unlink pgvector && brew link pgvector
```

Create a user
```bash
psql -h localhost -U postgres
ALTER USER postgres WITH PASSWORD 'Set_your_password_here';
CREATE EXTENSION IF NOT EXISTS vector;
```
## CHANGELOG

#### 0.1.3

Fixing imports

Changed output format of `basic_retrieval_chain` (`docs` key is now a list of `Document` objects, rather than a dict)

Unit tests for `basic_retrieval_chain`

#### 0.1.2

Unit tests

First Langgraph chain

#### 0.1.1

Initial Release

---
## 📄 License

chATLAS_Benchmark is released under Apache v2.0 license.

---

<div align="center">

**Made with ❤️ by the ATLAS Collaboration**

*For questions and support, please [contact](mailto:joseph.caimin.egan@cern.ch)*

</div>