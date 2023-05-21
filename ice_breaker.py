from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from dotenv import load_dotenv
import os

name="Elon Musk"
if __name__ == "__main__":
    # Load .env file with environment variables
    load_dotenv()
    
    print("Hello Langchain")
    # Get the Linkedin profile URL using an agent
    # For testing we use a fixed Linkedin profile publish in Gist
    # linkedin_profile_url = linkedin_lookup_agent(name="Eden Marco Udemy")
    linkedin_profile_url = "https://gist.githubusercontent.com/abelard-sf/3656866f16a84322dc807674c09c5384/raw/5d504661ff5b195d57216f7a0f3756c5143fc19d/eden-marco.json"
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    # summary_template = """
    #      given the Linkedin information {information} about a person from I want you to create:
    #      1. a short summary
    #      2. two interesting facts about them
    # """

    # summary_prompt_template = PromptTemplate(
    #     input_variables=["information"], template=summary_template
    # )

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url)
    # print(chain.run(information=linkedin_data))
    
    summary_template = """
         given the Linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
         3. A topic that may interest them
         4. 2 creative Ice breakers to open a conversation with them 
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
    )

    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print(chain.run(linkedin_information=linkedin_data, twitter_information=tweets))