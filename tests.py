#!/usr/bin/env python3
"""
Unit tests for JobCraft components.
"""

import unittest
import tempfile
import json
from pathlib import Path
from jobcraft.parsers import ResumeParser, JobDescriptionParser
from jobcraft.utils import JSONConverter, PDFGenerator


class TestParsers(unittest.TestCase):
    """Test resume and job description parsers."""
    
    def test_resume_parser_txt(self):
        """Test parsing a text resume."""
        parser = ResumeParser("examples/sample_resume.txt")
        resume = parser.parse()
        
        self.assertIn("name", resume)
        self.assertEqual(resume["name"], "John Doe")
        self.assertIn("contact", resume)
        self.assertIn("sections", resume)
        self.assertTrue(len(resume["sections"]) > 0)
    
    def test_job_parser_text(self):
        """Test parsing a job description from text."""
        with open("examples/sample_job_description.txt", 'r') as f:
            job_text = f.read()
        
        parser = JobDescriptionParser(job_text)
        job = parser.parse()
        
        self.assertIn("company", job)
        self.assertIn("position", job)
        self.assertEqual(job["company"], "InnovateTech Solutions")
        self.assertEqual(job["position"], "Senior Full-Stack Developer")
    
    def test_resume_parser_missing_file(self):
        """Test that parser raises error for missing file."""
        with self.assertRaises(FileNotFoundError):
            ResumeParser("nonexistent_file.txt")


class TestJSONConverter(unittest.TestCase):
    """Test JSON conversion utilities."""
    
    def test_dict_to_json(self):
        """Test converting dict to JSON string."""
        data = {"name": "Test", "value": 123}
        converter = JSONConverter()
        json_str = converter.dict_to_json(data)
        
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["name"], "Test")
        self.assertEqual(parsed["value"], 123)
    
    def test_dict_to_json_file(self):
        """Test saving dict to JSON file."""
        data = {"test": "data"}
        converter = JSONConverter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            converter.dict_to_json(data, temp_path)
            self.assertTrue(Path(temp_path).exists())
            
            # Read it back
            loaded = converter.json_to_dict(temp_path)
            self.assertEqual(loaded["test"], "data")
        finally:
            Path(temp_path).unlink()
    
    def test_json_to_dict_string(self):
        """Test converting JSON string to dict."""
        json_str = '{"key": "value"}'
        converter = JSONConverter()
        data = converter.json_to_dict(json_str)
        
        self.assertEqual(data["key"], "value")


class TestPDFGenerator(unittest.TestCase):
    """Test PDF generation utilities."""
    
    def test_generate_resume_pdf(self):
        """Test generating a resume PDF."""
        resume_data = {
            "name": "Test User",
            "contact": {
                "email": "test@example.com",
                "phone": "123-456-7890"
            },
            "summary": "Test summary",
            "experience": ["Job 1", "Job 2"],
            "education": ["Degree 1"],
            "skills": ["Python", "Java"]
        }
        
        generator = PDFGenerator()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate_resume_pdf(resume_data, temp_path)
            self.assertTrue(Path(temp_path).exists())
            self.assertGreater(Path(temp_path).stat().st_size, 0)
        finally:
            Path(temp_path).unlink()
    
    def test_generate_cover_letter_pdf(self):
        """Test generating a cover letter PDF."""
        cover_letter_data = {
            "applicant_name": "Test User",
            "applicant_email": "test@example.com",
            "company": "Test Company",
            "position": "Test Position",
            "content": "This is a test cover letter content."
        }
        
        generator = PDFGenerator()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate_cover_letter_pdf(cover_letter_data, temp_path)
            self.assertTrue(Path(temp_path).exists())
            self.assertGreater(Path(temp_path).stat().st_size, 0)
        finally:
            Path(temp_path).unlink()
    
    def test_generate_combined_pdf(self):
        """Test generating a combined PDF."""
        resume_data = {
            "name": "Test User",
            "contact": {"email": "test@example.com"},
            "summary": "Test",
            "experience": [],
            "education": [],
            "skills": []
        }
        
        cover_letter_data = {
            "applicant_name": "Test User",
            "applicant_email": "test@example.com",
            "company": "Test Company",
            "position": "Test Position",
            "content": "Test content"
        }
        
        generator = PDFGenerator()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate_combined_pdf(resume_data, cover_letter_data, temp_path)
            self.assertTrue(Path(temp_path).exists())
            self.assertGreater(Path(temp_path).stat().st_size, 0)
        finally:
            Path(temp_path).unlink()


class TestWorkflow(unittest.TestCase):
    """Test complete workflow integration."""
    
    def test_complete_pipeline(self):
        """Test the complete resume → dict → JSON → PDF workflow."""
        # Parse resume
        resume_parser = ResumeParser("examples/sample_resume.txt")
        resume_dict = resume_parser.parse()
        self.assertIsInstance(resume_dict, dict)
        
        # Parse job
        with open("examples/sample_job_description.txt", 'r') as f:
            job_text = f.read()
        job_parser = JobDescriptionParser(job_text)
        job_dict = job_parser.parse()
        self.assertIsInstance(job_dict, dict)
        
        # Convert to JSON
        converter = JSONConverter()
        json_str = converter.dict_to_json(resume_dict)
        self.assertIsInstance(json_str, str)
        
        # Convert back to dict
        loaded_dict = converter.json_to_dict(json_str)
        self.assertEqual(loaded_dict["name"], resume_dict["name"])
        
        # Generate PDF
        generator = PDFGenerator()
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.generate_resume_pdf(resume_dict, temp_path)
            self.assertTrue(Path(temp_path).exists())
        finally:
            Path(temp_path).unlink()


if __name__ == '__main__':
    unittest.main()
