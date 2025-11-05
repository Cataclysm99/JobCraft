"""
Resume parser module to extract resume data from various file formats (PDF, DOCX, TXT)
and convert to a Python dictionary structure.
"""

import os
from pathlib import Path
from typing import Dict, Any
import PyPDF2
from docx import Document


class ResumeParser:
    """Parse resume files and convert to structured dictionary."""
    
    def __init__(self, file_path: str):
        """
        Initialize the resume parser.
        
        Args:
            file_path: Path to the resume file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        self.file_extension = self.file_path.suffix.lower()
        self.raw_text = ""
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the resume file and return structured data as a dictionary.
        
        Returns:
            Dictionary containing parsed resume data
        """
        # Extract text based on file format
        if self.file_extension == '.pdf':
            self.raw_text = self._parse_pdf()
        elif self.file_extension in ['.docx', '.doc']:
            self.raw_text = self._parse_docx()
        elif self.file_extension == '.txt':
            self.raw_text = self._parse_txt()
        else:
            raise ValueError(f"Unsupported file format: {self.file_extension}")
        
        # Convert to structured dictionary
        return self._text_to_dict()
    
    def _parse_pdf(self) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def _parse_docx(self) -> str:
        """Extract text from DOCX file."""
        doc = Document(self.file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _parse_txt(self) -> str:
        """Extract text from TXT file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _text_to_dict(self) -> Dict[str, Any]:
        """
        Convert raw text to structured dictionary.
        This is a basic implementation that can be enhanced with NLP.
        
        Returns:
            Structured resume data dictionary
        """
        lines = [line.strip() for line in self.raw_text.split('\n') if line.strip()]
        
        # Basic structure - this can be enhanced with ML/NLP for better parsing
        resume_dict = {
            "name": "",
            "contact": {
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": "",
                "github": ""
            },
            "summary": "",
            "experience": [],
            "education": [],
            "skills": [],
            "raw_text": self.raw_text,
            "sections": {}
        }
        
        # Simple heuristic parsing
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower()
            
            # Detect sections
            if any(keyword in line_lower for keyword in ['experience', 'employment', 'work history']):
                if current_section and section_content:
                    resume_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "experience"
                section_content = []
            elif any(keyword in line_lower for keyword in ['education', 'academic']):
                if current_section and section_content:
                    resume_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "education"
                section_content = []
            elif any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                if current_section and section_content:
                    resume_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "skills"
                section_content = []
            elif any(keyword in line_lower for keyword in ['summary', 'objective', 'profile']):
                if current_section and section_content:
                    resume_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "summary"
                section_content = []
            else:
                if current_section:
                    section_content.append(line)
                else:
                    # First few lines often contain contact info
                    if '@' in line and not resume_dict["contact"]["email"]:
                        resume_dict["contact"]["email"] = line
                    elif 'linkedin.com' in line_lower:
                        resume_dict["contact"]["linkedin"] = line
                    elif 'github.com' in line_lower:
                        resume_dict["contact"]["github"] = line
                    elif not resume_dict["name"] and len(line) < 50:
                        # Assume first short line is name
                        resume_dict["name"] = line
        
        # Save final section
        if current_section and section_content:
            resume_dict["sections"][current_section] = "\n".join(section_content)
        
        return resume_dict
