"""
Cover letter generator using langchain_openai to create tailored cover letters.
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


class CoverLetterGenerator:
    """Generate customized cover letters using langchain_openai."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the cover letter generator.
        
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
    
    def generate(self, resume_dict: Dict[str, Any], job_dict: Dict[str, Any]) -> str:
        """
        Generate a customized cover letter based on resume and job description.
        
        Args:
            resume_dict: Parsed resume data as dictionary
            job_dict: Parsed job description data as dictionary
            
        Returns:
            Cover letter as formatted text
        """
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["resume_data", "job_data"],
            template="""You are an expert cover letter writer. You will be given a resume and a job description.
Your task is to write a compelling, professional cover letter that highlights the candidate's 
qualifications for the specific position.

Resume Data:
{resume_data}

Job Description:
{job_data}

Instructions:
1. Address the letter to the hiring manager (use "Dear Hiring Manager" if name unknown)
2. Open with a strong statement about why you're interested in the position
3. Highlight 2-3 relevant experiences or achievements from the resume that match job requirements
4. Explain why you're a good fit for the company and position
5. Close with a call to action and professional sign-off
6. Keep the letter to 3-4 paragraphs, approximately 300-400 words
7. Use a professional, enthusiastic tone
8. Include specific details from both the resume and job description

Write the cover letter:"""
        )
        
        # Create chain using LCEL (LangChain Expression Language)
        chain = prompt_template | self.llm
        
        # Convert dicts to readable strings
        resume_str = json.dumps(resume_dict, indent=2)
        job_str = json.dumps(job_dict, indent=2)
        
        # Generate cover letter
        result = chain.invoke({"resume_data": resume_str, "job_data": job_str})
        cover_letter = result.content if hasattr(result, 'content') else str(result)
        
        return cover_letter.strip()
    
    def to_dict(self, cover_letter_text: str, resume_dict: Dict[str, Any], 
                job_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert cover letter text to dictionary format for consistency.
        
        Args:
            cover_letter_text: Generated cover letter text
            resume_dict: Resume data
            job_dict: Job description data
            
        Returns:
            Cover letter as dictionary
        """
        return {
            "applicant_name": resume_dict.get("name", ""),
            "applicant_email": resume_dict.get("contact", {}).get("email", ""),
            "company": job_dict.get("company", ""),
            "position": job_dict.get("position", ""),
            "content": cover_letter_text,
            "metadata": {
                "target_company": job_dict.get("company", ""),
                "target_position": job_dict.get("position", ""),
                "generated_from": "langchain_openai"
            }
        }
