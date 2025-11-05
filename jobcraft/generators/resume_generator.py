"""
Resume customization generator using langchain_openai to tailor resumes to job descriptions.
"""

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ResumeGenerator:
    """Generate customized resumes using langchain_openai."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the resume generator.
        
        Args:
            api_key: OpenAI API key (optional, can use env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=self.api_key
        )
    
    def generate(self, resume_dict: Dict[str, Any], job_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a customized resume based on job description.
        
        Args:
            resume_dict: Parsed resume data as dictionary
            job_dict: Parsed job description data as dictionary
            
        Returns:
            Customized resume as dictionary
        """
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["resume_data", "job_data"],
            template="""You are an expert resume writer. You will be given a resume and a job description.
Your task is to customize the resume to better match the job description while maintaining honesty and accuracy.

Resume Data:
{resume_data}

Job Description:
{job_data}

Instructions:
1. Tailor the resume summary/objective to align with the job requirements
2. Emphasize relevant skills and experience that match the job description
3. Reorder or highlight experiences that are most relevant to the position
4. Use keywords from the job description where appropriate
5. Keep all information truthful - do not add false experience or skills
6. Maintain professional formatting and structure

Return the customized resume as a JSON object with the following structure:
{{
    "name": "candidate name",
    "contact": {{"email": "", "phone": "", "location": "", "linkedin": "", "github": ""}},
    "summary": "tailored professional summary",
    "experience": ["experience item 1", "experience item 2"],
    "education": ["education item 1", "education item 2"],
    "skills": ["skill1", "skill2"],
    "target_company": "company name from job description",
    "target_position": "position from job description"
}}

Customized Resume (JSON only):"""
        )
        
        # Create chain using LCEL (LangChain Expression Language)
        chain = prompt_template | self.llm
        
        # Convert dicts to readable strings
        resume_str = json.dumps(resume_dict, indent=2)
        job_str = json.dumps(job_dict, indent=2)
        
        # Generate customized resume
        result = chain.invoke({"resume_data": resume_str, "job_data": job_str})
        result = result.content if hasattr(result, 'content') else str(result)
        
        # Parse the result as JSON
        try:
            # Clean up the result to extract JSON
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            result = result.strip()
            
            customized_resume = json.loads(result)
            return customized_resume
        except json.JSONDecodeError:
            # If parsing fails, return a structured version with the raw result
            return {
                "name": resume_dict.get("name", ""),
                "contact": resume_dict.get("contact", {}),
                "summary": result[:500],  # Use first 500 chars as summary
                "experience": resume_dict.get("experience", []),
                "education": resume_dict.get("education", []),
                "skills": resume_dict.get("skills", []),
                "target_company": job_dict.get("company", ""),
                "target_position": job_dict.get("position", ""),
                "raw_generated_text": result
            }
