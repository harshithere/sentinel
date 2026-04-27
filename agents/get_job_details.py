from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

class JobDetails(BaseModel):
    job_title: str = Field(description="The title of the job position")
    required_skills: list[str] = Field(description="List of required technical and soft skills")
    required_experience_years: float = Field(description="Minimum years of experience required for the role")
    key_responsibilities: list[str] = Field(description="Key responsibilities and duties of the role")

def get_job_details_agent(job_description: str) -> JobDetails:
    """
    Agent that extracts structured information from a raw job description text.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    structured_llm = llm.with_structured_output(JobDetails)
    
    prompt = f"""
    You are an expert technical recruiter. Your task is to analyze the following job description and extract 
    the core requirements and details into a structured format.
    
    Extract exactly what the company is looking for.
    
    Job Description:
    ---
    {job_description}
    ---
    """
    
    return structured_llm.invoke(prompt)
