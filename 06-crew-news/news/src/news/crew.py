from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
# from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingNews(BaseModel):
    """ A news that is trending """
    news: str = Field(description="Highlight of the story")
    reason: str = Field(description="Reason this story is trending")

class TrendingNewsList(BaseModel):
    """ List of multiple stories that are in the news """
    stories: List[TrendingNews] = Field(description="List of stories trending in the news")

class TrendingNewsResearch(BaseModel):
    """ Detailed research on a story """
    name: str = Field(description="Story name")
    accuracy: str = Field(description="Ensure that the story is factually correct and is not a hoax or myth")
    details: str = Field(description="Detailed research of the story. Include answers to Who, What, When, Where, Why, and How. Include short and long term impacts")

class TrendingNewsResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingNewsResearch] = Field(description="Comprehensive research on all trending news")


@CrewBase
class NewsPicker():
    """NewsPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_news_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_news_finder'],
                     tools=[SerperDevTool()])
    
    @agent
    def technology_researcher(self) -> Agent:
        return Agent(config=self.agents_config['technology_researcher'], 
                     tools=[SerperDevTool()])

    @agent
    def story_picker(self) -> Agent:
        # return Agent(config=self.agents_config['story_picker'],
        #              tools=[PushNotificationTool()], memory=True)
        return Agent(config=self.agents_config['story_picker'])
    
    @task
    def find_trending_news(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_news'],
            output_pydantic=TrendingNewsList,
        )

    @task
    def research_trending_news(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_news'],
            output_pydantic=TrendingNewsResearchList,
        )

    @task
    def pick_news_of_the_day(self) -> Task:
        return Task(
            config=self.tasks_config['pick_news_of_the_day'],
        )
    


    @crew
    def crew(self) -> Crew:
        """Creates the NewsPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            # memory=True,
            # # Long-term memory for persistent storage across sessions
            # long_term_memory = LongTermMemory(
            #     storage=LTMSQLiteStorage(
            #         db_path="./memory/long_term_memory_storage.db"
            #     )
            # ),
            # # Short-term memory for current context using RAG
            # short_term_memory = ShortTermMemory(
            #     storage = RAGStorage(
            #             embedder_config={
            #                 "provider": "openai",
            #                 "config": {
            #                     "model": 'text-embedding-3-small'
            #                 }
            #             },
            #             type="short_term",
            #             path="./memory/"
            #         )
            #     ),            # Entity memory for tracking key information about entities
            # entity_memory = EntityMemory(
            #     storage=RAGStorage(
            #         embedder_config={
            #             "provider": "openai",
            #             "config": {
            #                 "model": 'text-embedding-3-small'
            #             }
            #         },
            #         type="short_term",
            #         path="./memory/"
            #     )
            # ),
        )