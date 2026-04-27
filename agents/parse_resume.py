from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

class ParsedResume(BaseModel):
    name: str = Field(description="Full name of the candidate")
    skills: list[str] = Field(description="List of technical and soft skills extracted from the resume")
    experience_years: float = Field(description="Total years of professional experience, estimated if not explicitly stated")
    summary: str = Field(description="A brief professional summary of the candidate's profile")

def parse_resume_agent(resume_text: str) -> ParsedResume:
    """
    Agent that extracts structured information from a raw resume text.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    structured_llm = llm.with_structured_output(ParsedResume)
    
    prompt = f"""
    You are an expert technical recruiter and resume parser. 
    Your task is to analyze the following resume text and extract the key information into a structured format.
    
    If any information is missing, do your best to infer it from the context or leave it as an empty string / 0.
    
    Resume Text:
    ---
    {resume_text}
    ---
    """
    
    return structured_llm.invoke(prompt)
