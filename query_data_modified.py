import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Beantworte die Frage ausschliesslich im Kontext von:

{context}

---

Beantworte die Frage im Kontext von oben: {question}
"""


def main():
    # Lade explizit die Datei 'settings.env'
    load_dotenv("settings.env")

    # Holt den API-Schlüssel aus den Umgebungsvariablen
    openai_api_key = os.getenv("OPENAI_API_KEY")
    #print(openai_api_key)  # Teste, ob der API-Schlüssel erfolgreich geladen wurde


    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    print(f"Results:\n{results}")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(f"\nPrompt: {prompt}\nPrompt-Template: {prompt_template}")

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    myResponse = f"\n\n\n\nFrage: {query_text}\nAntwort:{response_text}"
    print(f"1. {formatted_response}\n")
    print(f"2. {myResponse}\n")
    #print(myResponse)


if __name__ == "__main__":
    main()
