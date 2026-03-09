import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import FileReadTool

from .tools.sendgrid_tool import SendGridTool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()

file_read_tool = FileReadTool(base_path="output")

@CrewBase
class Homework():
    
    """Homework Helper Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def maths_tutor(self) -> Agent:
        agent = Agent(
            config=self.agents_config['maths_tutor'],
            verbose=True
        )
        return agent

    @agent
    def english_tutor(self) -> Agent:
        agent = Agent(
            config=self.agents_config['english_tutor'],
            verbose=True
        )
        print(f"{agent.model_config}")
        # print(f"### Debater_against Agent at work using {agent.llm.model} model")
        return agent

    @agent
    def general_tutor(self) -> Agent:
        agent = Agent(
            config=self.agents_config['general_tutor'],
            verbose=True
        )
        return agent

    @agent
    def principal(self) -> Agent:
        agent = Agent(
            config=self.agents_config['principal'],
            verbose=True
        )
        return agent

    @agent
    def mail_composer(self) -> Agent:
        agent = Agent(
            config=self.agents_config['mail_composer'],
            tools=[file_read_tool],
            verbose=True
        )
        return agent

    @agent
    def mailer(self) -> Agent:
        agent = Agent(
            config=self.agents_config['mailer'],
            tools=[SendGridTool()], 
            memory=True,
            verbose=True
        )
        print(f"### Mailer Agent at work using {agent.llm.model} model")
        return agent

    @task
    def create_assignment(self) -> Task:
        return Task(
            config=self.tasks_config['create_assignment'],
        )

    @task
    def create_math_homework(self) -> Task:
        return Task(
            config=self.tasks_config['create_math_homework'],
        )

    @task
    def create_english_homework(self) -> Task:
        return Task(
            config=self.tasks_config['create_english_homework'],
        )

    @task
    def create_general_homework(self) -> Task:
        return Task(
            config=self.tasks_config['create_general_homework'],
        )

    @task
    def compose_email(self) -> Task:
        return Task(
            config=self.tasks_config['compose_email'],
        )
    
    @task
    def send_email(self) -> Task:
        return Task(
            config=self.tasks_config['send_email'],
            timeout=60
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        # principal = Agent(
        #     config=self.agents_config['principal'],
        #     allow_delegation=True
        # )

        c = Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            # manager_agent=principal,
            verbose=True
        )
        return c
