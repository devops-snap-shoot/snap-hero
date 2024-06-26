from typing import Dict, List, Optional, Tuple

import config
import tiktoken
from exa_py import Exa
from openai import OpenAI

exa = Exa(config.EXA_API_KEY)

# For now we use the sync openai client
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_text_chunks(
    query: str,
    url: str,
    num_sentences: int = 5,
    highlights_per_url: int = 3,
) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Return a list of text chunks from the given URL that are relevant to the query.
    """

    highlights_options = {
        "num_sentences": num_sentences,  # how long our highlights should be
        "highlights_per_url": highlights_per_url,
    }
    search_response = exa.search_and_contents(
        query,
        highlights=highlights_options,
        num_results=10,
        use_autoprompt=True,
        include_domains=[url],
    )

    chunks = ["\n".join(sr.highlights) for sr in search_response.results]
    url_to_highlights = {sr.url: sr.highlights for sr in search_response.results}

    return chunks, url_to_highlights


def generate_prompt_from_chuncks(chunks: List[str], query: str) -> str:
    """
    Generate a prompt from the given chunks and question.
    TODO: add a check on token lenght to avoid exceeding the max token length of the model.
    """
    assert len(chunks) > 0, "Chunks should not be empty"

    concatenated_chunks = ""
    for chunck in chunks:
        concatenated_chunks += chunck + "\n\n"

    prompt = f"""
Query: {query}
Read the following text and answer the query.
---------------------
{concatenated_chunks}
---------------------
Given the context information and not prior knowledge, answer the query.
Do not start your answer with something like Based on the provided context information...
Query: {query}
Answer: 
"""
    return prompt


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def invoke_llm(
    prompt: str,
    model_name: str = "gpt-3.5-turbo",
    previous_messages: Optional[List[Dict[str, str]]] = None,
) -> Optional[str]:
    """
    Invoke the language model with the given prompt and return the response.
    """
    if previous_messages is None:
        previous_messages = []
    completion = openai_client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant replying to questions given a context.",
            }
        ]
        + previous_messages
        + [
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    return completion.choices[0].message.content


def query2answer(
    query: str,
    url: str,
    session_messages: List[Dict[str, str]],
    session_id: str,
    model_name: str = "gpt-3.5-turbo",
) -> Tuple[str, List[str]]:
    """
    Given a query and an URL, return the answer to the query.
    """
    
    url_sources = []

    try:
        chuncks, url_to_highlights = get_text_chunks(query, url)
        url_sources = list(url_to_highlights.keys())
    
        prompt = generate_prompt_from_chuncks(chuncks, query)
        # TODO: add a check on token lenght to avoid exceeding the max token length of the model.
        llm_answer = invoke_llm(prompt, previous_messages=session_messages)
        if llm_answer is None:
            llm_answer = (
                "Sorry, I was not able to answer, the OpenAI API returned None."
            )
        
    except Exception as e:
       
        llm_answer = "Sorry, I was not able to answer. Either you setup a wrong URL or the URL is too new."

    
    return llm_answer, url_sources
