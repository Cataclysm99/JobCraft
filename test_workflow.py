#!/usr/bin/env python3
"""
Test script to verify the complete JobCraft workflow without requiring OpenAI API key.
This simulates the AI generation step with mock data.
"""

from pathlib import Path
from jobcraft.parsers import ResumeParser, JobDescriptionParser
from jobcraft.utils import JSONConverter, PDFGenerator


def test_complete_workflow():
    """Test the complete workflow: Resume → Dict → JSON → PDF"""
    
    print("=" * 60)
    print("JobCraft Workflow Test (Without OpenAI)")
    print("=" * 60)
    print()
    
    # Step 1: Parse resume
    print("📄 Step 1: Parsing resume...")
    resume_parser = ResumeParser("examples/sample_resume.txt")
    resume_dict = resume_parser.parse()
    print(f"   ✓ Successfully parsed resume: {resume_dict.get('name', 'Unknown')}")
    
    # Step 2: Parse job description
    print("\n📋 Step 2: Parsing job description...")
    with open("examples/sample_job_description.txt", 'r') as f:
        job_text = f.read()
    job_parser = JobDescriptionParser(job_text)
    job_dict = job_parser.parse()
    company = job_dict.get('company', 'Unknown Company')
    position = job_dict.get('position', 'Unknown Position')
    print(f"   ✓ Successfully parsed job: {position} at {company}")
    
    # Step 3: Simulate AI generation (mock data for testing)
    print("\n🤖 Step 3: Simulating AI customization...")
    customized_resume = {
        "name": resume_dict.get("name", ""),
        "contact": resume_dict.get("contact", {}),
        "summary": f"Experienced software engineer with 5+ years of expertise perfectly aligned with {company}'s needs for {position}. Proven track record in full-stack development, cloud computing, and delivering scalable solutions.",
        "experience": [
            "Senior Software Engineer at Tech Solutions Inc. (2021-Present): Led development of microservices architecture serving 1M+ users, perfectly matching the requirements for this role.",
            "Software Engineer at Digital Innovations LLC (2018-2020): Built RESTful APIs and optimized database performance by 40%, demonstrating strong backend skills."
        ],
        "education": [
            "Bachelor of Science in Computer Science, UC Berkeley (2014-2018), GPA: 3.7/4.0"
        ],
        "skills": [
            "Python", "JavaScript", "TypeScript", "React", "Django", "Flask",
            "AWS", "Docker", "Kubernetes", "PostgreSQL", "MongoDB", "Redis"
        ],
        "target_company": company,
        "target_position": position
    }
    print(f"   ✓ Resume customized for {position}")
    
    # Step 4: Simulate cover letter generation
    print("\n✉️  Step 4: Simulating cover letter generation...")
    cover_letter_text = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With over 5 years of professional software development experience and a proven track record of delivering scalable web applications, I am confident I would be a valuable addition to your team.

In my current role as Senior Software Engineer at Tech Solutions Inc., I have led the development of microservices architecture serving over 1 million users, utilizing Python, JavaScript, and React—technologies that align perfectly with your requirements. I have extensive experience with cloud platforms like AWS, container orchestration with Docker and Kubernetes, and implementing CI/CD pipelines that have reduced deployment time by 60%.

My expertise in building RESTful APIs and full-stack applications, combined with my strong foundation in both SQL and NoSQL databases, makes me well-suited for the challenges described in your job posting. I am particularly excited about the opportunity to contribute to {company}'s mission and work with your innovative team.

I would welcome the opportunity to discuss how my skills and experience align with your needs. Thank you for considering my application.

Sincerely,
{resume_dict.get('name', '')}"""
    
    cover_letter_dict = {
        "applicant_name": resume_dict.get("name", ""),
        "applicant_email": resume_dict.get("contact", {}).get("email", ""),
        "company": company,
        "position": position,
        "content": cover_letter_text,
        "metadata": {
            "target_company": company,
            "target_position": position,
            "generated_from": "mock_generator"
        }
    }
    print(f"   ✓ Cover letter generated")
    
    # Step 5: Convert to JSON
    print("\n🔄 Step 5: Converting to JSON...")
    json_converter = JSONConverter()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    resume_json_path = output_dir / "resume.json"
    cover_letter_json_path = output_dir / "cover_letter.json"
    
    json_converter.dict_to_json(customized_resume, str(resume_json_path))
    json_converter.dict_to_json(cover_letter_dict, str(cover_letter_json_path))
    print(f"   ✓ JSON files saved to {output_dir}")
    
    # Step 6: Generate PDF outputs
    print("\n📑 Step 6: Generating PDF documents...")
    pdf_generator = PDFGenerator()
    
    resume_pdf_path = output_dir / f"resume_{company.replace(' ', '_')}.pdf"
    cover_letter_pdf_path = output_dir / f"cover_letter_{company.replace(' ', '_')}.pdf"
    combined_pdf_path = output_dir / f"application_package_{company.replace(' ', '_')}.pdf"
    
    pdf_generator.generate_resume_pdf(customized_resume, str(resume_pdf_path))
    pdf_generator.generate_cover_letter_pdf(cover_letter_dict, str(cover_letter_pdf_path))
    pdf_generator.generate_combined_pdf(customized_resume, cover_letter_dict, str(combined_pdf_path))
    
    print(f"   ✓ Resume PDF saved: {resume_pdf_path}")
    print(f"   ✓ Cover letter PDF saved: {cover_letter_pdf_path}")
    print(f"   ✓ Combined PDF saved: {combined_pdf_path}")
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Complete workflow test passed.")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  - {resume_json_path}")
    print(f"  - {cover_letter_json_path}")
    print(f"  - {resume_pdf_path}")
    print(f"  - {cover_letter_pdf_path}")
    print(f"  - {combined_pdf_path}")
    print()


if __name__ == "__main__":
    test_complete_workflow()
