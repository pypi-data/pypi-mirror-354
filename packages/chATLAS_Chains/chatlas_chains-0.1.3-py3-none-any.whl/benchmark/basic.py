import os

from tqdm import tqdm

from chATLAS_Benchmark import BenchmarkTest
from chATLAS_Chains.chains.basic import basic_retrieval_chain
from chATLAS_Chains.prompt.starters import CHAT_PROMPT_TEMPLATE
from chATLAS_Chains.vectorstore import vectorstore

chain = basic_retrieval_chain(prompt=CHAT_PROMPT_TEMPLATE, vectorstore=vectorstore, model_name="gpt-4o-mini")

# Initialize the test set
questions_path = os.getenv("CHATLAS_BENCHMARK_QUESTIONS")
test = BenchmarkTest(questions_path)
# test = BenchmarkTest(questions_path, keys={"test_questions": "question", "test_documents":"documents", "test_answer": "answer"})

# --- Run the RAG on the questions ---
# Assuming RAG.run() returns an answer and list of docs for each question
gen_answers = []
gen_docs = []
for q in tqdm(test.questions):
    result = chain.invoke(q)

    gen_answers.append(result["answer"].content)
    gen_docs.append(result["docs"])

# Set generated answers and documents on the test instance
test.set_generated_data(gen_answers, gen_docs)

# Run the scoring with any metrics you want
scores = test.score_test_set("LexicalMetrics", "SemanticSimilarity", "DocumentMatch")

# Save the results to the db
test.store_results(scores, db_name="results.db", name="basic_retrieval_chain")
