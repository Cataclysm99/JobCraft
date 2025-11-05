# JobCraft Quick Reference

## Installation

```bash
# Clone the repository
git clone https://github.com/Cataclysm99/JobCraft.git
cd JobCraft

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Basic Usage

```bash
# Simple usage with text files
python main.py --resume examples/sample_resume.txt --job examples/sample_job_description.txt

# Using a PDF resume
python main.py --resume my_resume.pdf --job job_description.txt

# Using a job posting URL
python main.py --resume resume.docx --job https://example.com/careers/job-123

# Generate combined PDF
python main.py --resume resume.txt --job job.txt --combined

# Save intermediate JSON files
python main.py --resume resume.pdf --job job.txt --save-json

# Specify custom output directory
python main.py --resume resume.txt --job job.txt --output ./my_applications
```

## Workflow Diagram

```
Input: Resume File (PDF/DOCX/TXT) + Job Description (Text/URL)
    ↓
Step 1: Parse Resume → Extract text → Convert to Python Dict
    ↓
Step 2: Parse Job Description → Extract requirements → Convert to Python Dict
    ↓
Step 3: AI Processing (LangChain + OpenAI GPT)
    ↓
Step 4: Generate Customized Resume Dict + Cover Letter Dict
    ↓
Step 5: Convert to JSON (optional save)
    ↓
Step 6: Generate Professional PDFs
    ↓
Output: Custom Resume PDF + Cover Letter PDF (or Combined PDF)
```

## File Structure

```
JobCraft/
├── jobcraft/              # Main package
│   ├── parsers/          # Resume & job description parsing
│   ├── generators/       # AI-powered content generation
│   └── utils/            # JSON & PDF utilities
├── examples/             # Sample files for testing
├── output/              # Generated files (ignored by git)
├── main.py              # CLI interface
├── test_workflow.py     # Workflow demonstration
└── tests.py             # Unit tests
```

## Testing

```bash
# Run unit tests
python -m unittest tests -v

# Test complete workflow (without OpenAI API)
python test_workflow.py

# Test with actual OpenAI API
export OPENAI_API_KEY=your_key_here
python main.py --resume examples/sample_resume.txt --job examples/sample_job_description.txt
```

## Key Features

1. **Multi-format Support**: Parses PDF, DOCX, and TXT resumes
2. **URL Support**: Fetch job descriptions directly from career sites
3. **AI Customization**: Uses OpenAI GPT-3.5 to tailor content
4. **Clean Pipeline**: Dict → JSON → PDF workflow
5. **Professional Output**: Formatted PDFs with proper styling
6. **Flexible Options**: Separate or combined PDFs, optional JSON export

## Python API Usage

```python
from jobcraft.parsers import ResumeParser, JobDescriptionParser
from jobcraft.generators import ResumeGenerator, CoverLetterGenerator
from jobcraft.utils import JSONConverter, PDFGenerator

# Parse inputs
resume_parser = ResumeParser("resume.pdf")
resume_dict = resume_parser.parse()

job_parser = JobDescriptionParser("job_text_or_url")
job_dict = job_parser.parse()

# Generate customized content (requires OPENAI_API_KEY)
resume_gen = ResumeGenerator()
custom_resume = resume_gen.generate(resume_dict, job_dict)

cover_letter_gen = CoverLetterGenerator()
cover_letter = cover_letter_gen.generate(resume_dict, job_dict)
cover_letter_dict = cover_letter_gen.to_dict(cover_letter, resume_dict, job_dict)

# Convert to JSON
json_converter = JSONConverter()
json_converter.dict_to_json(custom_resume, "resume.json")

# Generate PDFs
pdf_gen = PDFGenerator()
pdf_gen.generate_resume_pdf(custom_resume, "resume.pdf")
pdf_gen.generate_cover_letter_pdf(cover_letter_dict, "cover_letter.pdf")
```

## Environment Variables

- `OPENAI_API_KEY`: Required for AI-powered content generation

## Output Files

When you run JobCraft, it generates:
- `resume_CompanyName.pdf` - Customized resume
- `cover_letter_CompanyName.pdf` - Personalized cover letter
- `application_package_CompanyName.pdf` - Combined PDF (with --combined)
- `resume.json` - Resume data (with --save-json)
- `cover_letter.json` - Cover letter data (with --save-json)

## Troubleshooting

**Issue**: `OpenAI API key not provided`
- **Solution**: Set `OPENAI_API_KEY` in your `.env` file or environment

**Issue**: `Module not found`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: `Resume file not found`
- **Solution**: Check the file path is correct and file exists

**Issue**: `Failed to fetch job description from URL`
- **Solution**: Verify the URL is accessible and contains job description content
