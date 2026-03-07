import os
from crewai import Agent, Crew, Process, Task, LLM

from .tools.sendgrid_tool import SendGridTool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()

llama3_2 = LLM(
    provider="ollama",
    model="llama3.1:latest",
    base_url="http://127.0.0.1:11434"
)


# @Tool
# def send_email_via_sendgrid(to_email: str, subject: str, content: str) -> str:
#     """Send an email using SendGrid."""
#     message = Mail(
#         # from_email=os.getenv("SENDGRID_FROM_EMAIL"),
#         from_email="mondalsushobhan@outlook.com",
#         to_emails="sushobhanmondal@gmail.com",
#         subject="some subject",
#         plain_text_content="some content"
#     )

#     try:
#         sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
#         response = sg.send(message)
#         return f"Email sent successfully with status {response.status_code}"
#     except Exception as e:
#         return f"Failed to send email: {str(e)}"

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
        print(f"### Debater_for Agent at work using {agent.llm.model} model")
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

        principal = Agent(
            config=self.agents_config['principal'],
            allow_delegation=True
        )

        c = Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=principal,
            verbose=True
        )
        return c
