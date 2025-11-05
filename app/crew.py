from typing import Any, Dict, List
from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
)
from app.tools.pdf_reader import PDFReaderTool


# ------------------------------------------------------------
# Pydantic models
# ------------------------------------------------------------
class CVData(BaseModel):
    id: str
    source_file: str
    role: str
    personal_info: Dict[str, Any]
    summary: str
    skills: Dict[str, Any]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Any]
    projects: List[Any]
    languages: List[Any]
    side_notes: str


class CVEligibilityResult(BaseModel):
    """Schema for candidate eligibility evaluation results."""
    decision: str
    match_score: float
    missing_must_have_skills: List[str]
    missing_education: bool
    experience_gap_years: float
    notes: str


# ------------------------------------------------------------
# Crew
# ------------------------------------------------------------
@CrewBase
class HRCrew():
    """HR Crew that: PDF -> TXT -> JSON -> Eligibility"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # ===================== AGENTS =====================

    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            verbose=True,
            tools=[
                DirectoryReadTool(),  # list files in folder_path
                PDFReaderTool(),      # read each PDF
                FileWriterTool(),     # write txt to output_path
            ],
            # llm=None  # uncomment if you want to guarantee no token usage here
        )

    @agent
    def cv_json_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_json_builder'],
            verbose=True,
            tools=[
                DirectoryReadTool(),  #
                FileReadTool(),
                FileWriterTool(),
            ],
        )

    @agent
    def cv_eligibility_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_eligibility_checker'],
            verbose=True,
            tools=[
                FileReadTool(),
                FileWriterTool(),
            ],
        )

    # ===================== TASKS =====================

    @task
    def cv_reader_task(self) -> Task:
        """
        Task 1: PDF -> TXT
        Uses {folder_path} and {output_path} from inputs.
        """
        return Task(
            config=self.tasks_config['cv_reader_task'],
            verbose=True,
        )

    @task
    def cv_json_builder_task(self) -> Task:
        """
        Task 2: TXT -> CVData JSON
        Reads txts from {output_path} and writes candidate JSONs there too.
        """
        return Task(
            config=self.tasks_config['cv_json_builder_task'],
            verbose=True,
            output_json=CVData,
        )

    @task
    def check_candidate_eligibility_task(self) -> Task:
        """
        Task 3: Candidate JSON -> Eligibility decision
        Uses candidate JSONs + job_json from inputs.
        """
        return Task(
            config=self.tasks_config['check_candidate_eligibility_task'],
            verbose=True,
            output_json=CVEligibilityResult,
            context=[self.cv_json_builder_task()]
        )

    # ===================== CREW =====================

    @crew
    def crew(self) -> Crew:
        """Creates the HR crew with 3 sequential tasks."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
