"""
Job description parser module to extract job information from text or URLs.
"""

import re
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup


class JobDescriptionParser:
    """Parse job descriptions from text or web URLs."""
    
    def __init__(self, source: str):
        """
        Initialize the job description parser.
        
        Args:
            source: Either a job description text or a URL to a job posting
        """
        self.source = source
        self.is_url = self._is_url(source)
        self.raw_text = ""
        
    def _is_url(self, text: str) -> bool:
        """Check if the source is a URL."""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(text))
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse the job description and return structured data.
        
        Returns:
            Dictionary containing parsed job description data
        """
        if self.is_url:
            self.raw_text = self._fetch_from_url()
        else:
            self.raw_text = self.source
        
        return self._text_to_dict()
    
    def _fetch_from_url(self) -> str:
        """Fetch job description from URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.source, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise ValueError(f"Failed to fetch job description from URL: {e}")
    
    def _text_to_dict(self) -> Dict[str, Any]:
        """
        Convert raw job description text to structured dictionary.
        
        Returns:
            Structured job description data
        """
        lines = [line.strip() for line in self.raw_text.split('\n') if line.strip()]
        
        job_dict = {
            "company": "",
            "position": "",
            "location": "",
            "description": "",
            "requirements": [],
            "responsibilities": [],
            "skills": [],
            "raw_text": self.raw_text,
            "sections": {}
        }
        
        # Extract company name and position (basic heuristics)
        for line in lines[:20]:  # Check first 20 lines
            line_lower = line.lower()
            if 'company' in line_lower and not job_dict["company"]:
                job_dict["company"] = line.split(':')[-1].strip() if ':' in line else line
            if any(word in line_lower for word in ['position', 'title', 'role', 'job']) and not job_dict["position"]:
                job_dict["position"] = line.split(':')[-1].strip() if ':' in line else line
            if 'location' in line_lower and not job_dict["location"]:
                job_dict["location"] = line.split(':')[-1].strip() if ':' in line else line
        
        # Parse sections
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in ['requirements', 'qualifications', 'required']):
                if current_section and section_content:
                    job_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "requirements"
                section_content = []
            elif any(keyword in line_lower for keyword in ['responsibilities', 'duties', 'what you']):
                if current_section and section_content:
                    job_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "responsibilities"
                section_content = []
            elif any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                if current_section and section_content:
                    job_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "skills"
                section_content = []
            elif any(keyword in line_lower for keyword in ['description', 'about', 'overview']):
                if current_section and section_content:
                    job_dict["sections"][current_section] = "\n".join(section_content)
                current_section = "description"
                section_content = []
            else:
                if current_section:
                    section_content.append(line)
        
        # Save final section
        if current_section and section_content:
            job_dict["sections"][current_section] = "\n".join(section_content)
        
        # Fill in description if empty
        if not job_dict["description"] and job_dict["raw_text"]:
            job_dict["description"] = job_dict["raw_text"][:500]  # First 500 chars
        
        return job_dict
