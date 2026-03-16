import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import FileReadTool

from .tools.sendgrid_tool import SendGridTool
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()

file_read_tool = FileReadTool(base_path="output")

@CrewBase
class Homework():
    """Homework Helper Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ⭐ CrewBase automatically calls this when kickoff(inputs=...) is used
    def set_inputs(self, inputs: dict):
        self.topic = inputs.get("topic")
        self.grade = inputs.get("grade")
        self.to_email = inputs.get("to_email")

    # -------------------------
    # Agents
    # -------------------------

    @agent
    def maths_tutor(self) -> Agent:
        return Agent(config=self.agents_config['maths_tutor'], verbose=True)

    @agent
    def english_tutor(self) -> Agent:
        return Agent(config=self.agents_config['english_tutor'], verbose=True)

    @agent
    def general_tutor(self) -> Agent:
        return Agent(config=self.agents_config['general_tutor'], verbose=True)

    @agent
    def principal(self) -> Agent:
        return Agent(config=self.agents_config['principal'], verbose=True)

    @agent
    def mail_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['mail_composer'],
            tools=[file_read_tool],
            verbose=True
        )

    @agent
    def mailer(self) -> Agent:
        return Agent(
            config=self.agents_config['mailer'],
            tools=[SendGridTool(), file_read_tool],
            memory=True,
            verbose=True
        )

    # -------------------------
    # Tasks (YAML-backed)
    # -------------------------

    @task
    def create_math_homework(self) -> Task:
        return Task(config=self.tasks_config['create_math_homework'])

    @task
    def create_english_homework(self) -> Task:
        return Task(config=self.tasks_config['create_english_homework'])

    @task
    def create_general_homework(self) -> Task:
        return Task(config=self.tasks_config['create_general_homework'])

    @task
    def compose_email(self) -> Task:
        return Task(config=self.tasks_config['compose_email'])

    @task
    def send_email(self) -> Task:
        return Task(config=self.tasks_config['send_email'], timeout=60)

    # -------------------------
    # MAIN CREW (principal runs first)
    # -------------------------

    @crew
    def crew(self) -> Crew:
        """Main Homework Crew with principal routing inside the same crew."""

        # 1. Build the principal task FIRST
        principal_task = Task(
            config=self.tasks_config['principal_task'],
            agent=self.principal()
        )

        # 2. Placeholder tutor task — will be replaced dynamically
        #    We create a dummy task so CrewAI accepts the task list.
        routing_placeholder = Task(
            description="This task will be replaced dynamically after principal decision.",
            agent=self.general_tutor()
        )

        # 3. Compose + send tasks
        compose_task = Task(
            config=self.tasks_config['compose_email'],
            agent=self.mail_composer()
        )

        send_task = Task(
            config=self.tasks_config['send_email'],
            agent=self.mailer()
        )

        # 4. Build the crew with ALL tasks in order
        crew = Crew(
            agents=[
                self.principal(),
                self.maths_tutor(),
                self.english_tutor(),
                self.general_tutor(),
                self.mail_composer(),
                self.mailer()
            ],
            tasks=[
                principal_task,       # runs first
                routing_placeholder,  # will be replaced dynamically
                compose_task,
                send_task
            ],
            process=Process.sequential,
            verbose=True
        )

        # ⭐ Dynamic routing hook
        @crew.on_task_complete(principal_task)
        def route_after_principal(result, task, crew_instance):
            import json
            decision = json.loads(str(result).strip())
            selected = decision["selected_tutor"]

            # Pick correct tutor task
            if selected == "maths_tutor":
                new_task = Task(
                    config=self.tasks_config['create_math_homework'],
                    agent=self.maths_tutor()
                )
            elif selected == "english_tutor":
                new_task = Task(
                    config=self.tasks_config['create_english_homework'],
                    agent=self.english_tutor()
                )
            else:
                new_task = Task(
                    config=self.tasks_config['create_general_homework'],
                    agent=self.general_tutor()
                )

            # Replace placeholder with the correct tutor task
            crew_instance.replace_task(routing_placeholder, new_task)

        return crew