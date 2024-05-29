# Function to query the Hugging Face model API
import streamlit as st
import requests
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# Function to query the Hugging Face model API
def query_huggingface(prompt, styles):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
    
    style_prompt = ', '.join(styles)  # Combine all selected styles into one string
    full_prompt = f"{style_prompt} {prompt}"
    
    request_payload = {
        "inputs": full_prompt
    }

    response = requests.post(API_URL, headers=headers, json=request_payload)
    return response.content



#Select Model 
#llm = Ollama(model="mistral:latest", verbose=True)
llm  = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

# Exa Search API
@tool
def exa_search_api(query: str) -> str:
    """Use this tool to search for latest information on the internet."""
    url = "https://api.exa.ai/search"

    payload = {
        "query": query,
        "contents": {"text": {"includeHtmlTags": False}},
        "numResults": 3,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": st.secrets["EXA_API_KEY"],
    }
    response = requests.post(url, json=payload, headers=headers)

    return response.text


web_tool = WebsiteSearchTool()
search_tool = exa_search_api

def kickoffTheCrew(topic, styles):
    # Dictionary mapping styles to agent configurations
    agent_roles = {
        'Blog': {
            'role': 'Blogger',
            'goal': 'Write an engaging and interesting blog.',
            'backstory': 'You are an Expert Blogger on the Internet.',
            'details': 'Include relevant examples, provide tutorial-type instructions, and ensure the blog style is evident.'
        },
        'Poem': {
            'role': 'Poet',
            'goal': 'Compose a thoughtful and expressive poem.',
            'backstory': 'You are a Poet with a deep appreciation for aesthetics and rhythm.',
            'details': 'Focus on the beauty of words and the flow of verses.'
        },
        'Joke': {
            'role': 'Humorist',
            'goal': 'Craft a funny and entertaining joke.',
            'backstory': 'You are a Humorist who brings laughter and joy through your writing.',
            'details': 'Keep the content light-hearted and humorous without any technical content.'
        },
        'Essay': {
            'role': 'Essayist',
            'goal': 'Develop a well-argued and cohesive essay.',
            'backstory': 'You are an Essayist with a knack for critical thinking and clear expression.',
            'details': 'Include in-depth analysis and ensure clear presentation of arguments.'
        }
    }

    # Assume only one style is selected, default to 'Blog' if none is provided
    primary_style = styles if styles else 'Blog'
    agent_config = agent_roles.get(primary_style, agent_roles['Blog'])  # Use primary style
    
    researcher = Agent(
        role="Internet Research",
        goal=f"Perform research on {topic}, focusing on {primary_style}. Find and explore detailed content about {topic} with an emphasis on {primary_style}.",
        verbose=True,
        llm=llm,
        backstory=f"You are an expert Internet Researcher specialized in {primary_style}."
    )

    agent = Agent(
        role=agent_config['role'],
        goal=(f"{agent_config['goal']} in maximum 1000 words. "
              "Add relevant emojis if appropriate, and ensure the style "
              f"{primary_style} is prominently featured throughout."),
        verbose=True,
        allow_delegation=True,
        llm=llm,
        backstory=(f"{agent_config['backstory']} "
                    f"{agent_config['details']}")
    )
    
    critic = Agent(
        role='Expert Writing Critic',
        goal=(f"Provide feedback and criticize {primary_style} drafts. "
              "Make sure that the tone and writing style is compelling, "
              "simple and concise."),
        verbose=True,
        allow_delegation=True,
        llm=llm,
        backstory=(f"You are an expert at providing feedback to the "
                    f"{primary_style} agent. You can tell when a "
                    f"{primary_style} isn't concise, simple or engaging enough. "
                    "You know how to provide helpful feedback that "
                    f"can improve any {primary_style}.")
    )
    
    task_search = Task(
        description=f"Search for all the details about {topic} in a {primary_style} manner. Your final answer must be a consolidated content that can be used for {agent_config['role']} and should reflect the {primary_style}.",
        expected_output=f"A comprehensive no more than 10000 words information about {topic} in the style of {primary_style}",
        max_inter=3,
        tools=[search_tool, web_tool],
        agent=researcher)

    task_post = Task(
        description=f"Write a well-structured {primary_style} {agent_config['role']} and at maximum 10000 words. The {agent_config['role']} should also reflect the core essence of {primary_style}.",
        expected_output=f"A comprehensive less than 10 paragraph {primary_style} on {topic} in markdown format",
        agent=agent)
    
    task_critique = Task(
    description=f"Identify parts of the {primary_style} that aren't written concise "
                 f"enough and rewrite and change them. Make sure that the {primary_style} "
                 "has an engaging headline with 30 characters max, and that there are no more than 10 paragraphs.",
    expected_output=(f"A comprehensive less than 10 paragraph {primary_style} on {topic} in markdown format"),
    agent=critic)

    crew = Crew(
        agents=[researcher, agent, critic],
        tasks=[task_search, task_post, task_critique],
        verbose=2,
        process=Process.sequential)

    result = crew.kickoff()
    return result


