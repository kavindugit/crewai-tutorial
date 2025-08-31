import yaml
from crewai import Agent , Crew , Process , Task , LLM
from crewai.project import CrewBase, agent , crew , task
from crewai_tools import SerperDevTool , ScrapeWebsiteTool , DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class BlogCrew():
    """Blog writing crew"""

    def __init__(self):
        # Load YAML configs into dictionaries
        with open("config/agents.yaml", "r") as f:
            self.agent_config = yaml.safe_load(f)

        with open("config/tasks.yaml", "r") as f:
            self.task_config = yaml.safe_load(f)

    @agent
    def researcher(self) -> Agent :
        return Agent(
            config = self.agent_config['research_agent'] , # type: ignore[index]
            tools = [SerperDevTool()],
            verbose = True,
        )
    @agent
    def writer(self) -> Agent :
        return Agent(
            config = self.agent_config['writer_agent'] , # type: ignore[index]
            verbose = True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.task_config['research_task'], # type: ignore[index]
            agent=self.researcher(),
        )
    @task
    def blog_task(self) -> Task:
        return Task(
            config=self.task_config['blog_task'], # type: ignore[index]
            agent=self.writer(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = [self.researcher(), self.writer()],
            tasks = [self.research_task(), self.blog_task()],

        )
if __name__== "__main__":
    blog_crew = BlogCrew()
    blog_crew.crew().kickoff(inputs ={"topic":"IT industry in next 10 years"})

