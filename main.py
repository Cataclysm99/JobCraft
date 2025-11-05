#!/usr/bin/env python3
"""
JobCraft - Main CLI interface for generating custom resumes and cover letters.

This tool accepts:
- Resume file (PDF, DOCX, TXT)
- Job description (text or URL)

And outputs:
- Customized resume (PDF)
- Cover letter (PDF)

Workflow: Resume File → Parser → Dict → LangChain → JSON → PDF
"""

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

from jobcraft.parsers import ResumeParser, JobDescriptionParser
from jobcraft.generators import ResumeGenerator, CoverLetterGenerator
from jobcraft.utils import JSONConverter, PDFGenerator

# Load environment variables
load_dotenv()


def main():
    """Main entry point for JobCraft CLI."""
    parser = argparse.ArgumentParser(
        description="JobCraft - Generate custom resumes and cover letters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from resume file and job description text
  python main.py --resume my_resume.pdf --job "Software Engineer at TechCorp..."
  
  # Generate from resume file and job posting URL
  python main.py --resume my_resume.docx --job https://example.com/job-posting
  
  # Specify custom output directory
  python main.py --resume resume.txt --job job_desc.txt --output ./output
        """
    )
    
    parser.add_argument(
        "--resume", "-r",
        required=True,
        help="Path to resume file (PDF, DOCX, or TXT)"
    )
    
    parser.add_argument(
        "--job", "-j",
        required=True,
        help="Job description (text or URL to job posting)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Output directory for generated files (default: ./output)"
    )
    
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save intermediate JSON files"
    )
    
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Generate a single PDF with both cover letter and resume"
    )
    
    args = parser.parse_args()
    
    # Validate resume file exists
    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"Error: Resume file not found: {args.resume}")
        sys.exit(1)
    
    # Check if job is a file path
    job_source = args.job
    job_path = Path(args.job)
    if job_path.exists():
        with open(job_path, 'r', encoding='utf-8') as f:
            job_source = f.read()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("JobCraft - Custom Resume and Cover Letter Generator")
    print("=" * 60)
    print()
    
    # Step 1: Parse resume
    print("📄 Step 1: Parsing resume...")
    try:
        resume_parser = ResumeParser(str(resume_path))
        resume_dict = resume_parser.parse()
        print(f"   ✓ Successfully parsed resume: {resume_dict.get('name', 'Unknown')}")
    except Exception as e:
        print(f"   ✗ Error parsing resume: {e}")
        sys.exit(1)
    
    # Step 2: Parse job description
    print("\n📋 Step 2: Parsing job description...")
    try:
        job_parser = JobDescriptionParser(job_source)
        job_dict = job_parser.parse()
        company = job_dict.get('company', 'Unknown Company')
        position = job_dict.get('position', 'Unknown Position')
        print(f"   ✓ Successfully parsed job: {position} at {company}")
    except Exception as e:
        print(f"   ✗ Error parsing job description: {e}")
        sys.exit(1)
    
    # Step 3: Generate customized resume using LangChain
    print("\n🤖 Step 3: Generating customized resume with AI...")
    try:
        resume_generator = ResumeGenerator()
        customized_resume = resume_generator.generate(resume_dict, job_dict)
        print(f"   ✓ Resume customized for {customized_resume.get('target_position', position)}")
    except Exception as e:
        print(f"   ✗ Error generating resume: {e}")
        print("   ℹ️  Make sure OPENAI_API_KEY is set in your environment")
        sys.exit(1)
    
    # Step 4: Generate cover letter using LangChain
    print("\n✉️  Step 4: Generating cover letter with AI...")
    try:
        cover_letter_generator = CoverLetterGenerator()
        cover_letter_text = cover_letter_generator.generate(resume_dict, job_dict)
        cover_letter_dict = cover_letter_generator.to_dict(cover_letter_text, resume_dict, job_dict)
        print(f"   ✓ Cover letter generated")
    except Exception as e:
        print(f"   ✗ Error generating cover letter: {e}")
        print("   ℹ️  Make sure OPENAI_API_KEY is set in your environment")
        sys.exit(1)
    
    # Step 5: Convert to JSON (optional save)
    print("\n🔄 Step 5: Converting to JSON...")
    json_converter = JSONConverter()
    
    if args.save_json:
        resume_json_path = output_dir / "resume.json"
        cover_letter_json_path = output_dir / "cover_letter.json"
        
        json_converter.dict_to_json(customized_resume, str(resume_json_path))
        json_converter.dict_to_json(cover_letter_dict, str(cover_letter_json_path))
        print(f"   ✓ JSON files saved to {output_dir}")
    else:
        print(f"   ✓ JSON conversion complete (not saved)")
    
    # Step 6: Generate PDF outputs
    print("\n📑 Step 6: Generating PDF documents...")
    pdf_generator = PDFGenerator()
    
    try:
        if args.combined:
            # Generate combined PDF
            combined_path = output_dir / f"application_package_{company.replace(' ', '_')}.pdf"
            pdf_generator.generate_combined_pdf(customized_resume, cover_letter_dict, str(combined_path))
            print(f"   ✓ Combined PDF saved: {combined_path}")
        else:
            # Generate separate PDFs
            resume_pdf_path = output_dir / f"resume_{company.replace(' ', '_')}.pdf"
            cover_letter_pdf_path = output_dir / f"cover_letter_{company.replace(' ', '_')}.pdf"
            
            pdf_generator.generate_resume_pdf(customized_resume, str(resume_pdf_path))
            pdf_generator.generate_cover_letter_pdf(cover_letter_dict, str(cover_letter_pdf_path))
            
            print(f"   ✓ Resume PDF saved: {resume_pdf_path}")
            print(f"   ✓ Cover letter PDF saved: {cover_letter_pdf_path}")
    except Exception as e:
        print(f"   ✗ Error generating PDFs: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Your customized application materials are ready.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
