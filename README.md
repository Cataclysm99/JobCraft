# JobCraft

Tools for efficiently crafting custom resumes and cover letters from job descriptions to make job applications much easier, streamlined, and catered to the needs of the company and job position.

## Features

- **Multi-format Resume Parsing**: Supports PDF, DOCX, and TXT resume files
- **Job Description Parsing**: Accepts job descriptions as text or URLs to job postings
- **AI-Powered Customization**: Uses OpenAI's GPT models via LangChain to tailor resumes and generate cover letters
- **Structured Workflow**: Resume → Dict → JSON → PDF pipeline for clean data processing
- **Professional PDF Output**: Generates beautifully formatted resume and cover letter PDFs

## Workflow

```
Resume File (PDF/DOCX/TXT)
    ↓
Parse to Python Dict
    ↓
AI Processing with LangChain + Job Description
    ↓
Convert to JSON
    ↓
Generate PDF Output
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Cataclysm99/JobCraft.git
cd JobCraft
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

Generate customized resume and cover letter from a resume file and job description:

```bash
python main.py --resume examples/sample_resume.txt --job examples/sample_job_description.txt
```

### Using a Job Posting URL

```bash
python main.py --resume my_resume.pdf --job https://example.com/careers/job-posting
```

### Generate Combined PDF

Create a single PDF with both cover letter and resume:

```bash
python main.py --resume resume.docx --job job_description.txt --combined
```

### Save Intermediate JSON Files

```bash
python main.py --resume resume.pdf --job job_desc.txt --save-json
```

### Custom Output Directory

```bash
python main.py --resume resume.txt --job job.txt --output ./my_applications
```

## Command-Line Options

```
--resume, -r    Path to resume file (required)
--job, -j       Job description text or URL (required)
--output, -o    Output directory (default: ./output)
--save-json     Save intermediate JSON files
--combined      Generate single PDF with both documents
```

## Project Structure

```
JobCraft/
├── jobcraft/
│   ├── parsers/
│   │   ├── resume_parser.py      # Parse resume files
│   │   └── job_parser.py         # Parse job descriptions
│   ├── generators/
│   │   ├── resume_generator.py   # Generate custom resumes with AI
│   │   └── cover_letter_generator.py  # Generate cover letters with AI
│   └── utils/
│       ├── json_converter.py     # Dict ↔ JSON conversion
│       └── pdf_generator.py      # PDF generation
├── examples/
│   ├── sample_resume.txt
│   └── sample_job_description.txt
├── output/                        # Generated files
├── main.py                        # CLI interface
└── requirements.txt
```

## How It Works

1. **Resume Parsing**: Extracts text from various file formats and converts to structured dictionary
2. **Job Description Parsing**: Extracts job information from text or web URLs
3. **AI Customization**: Uses LangChain with OpenAI to:
   - Tailor resume content to match job requirements
   - Generate personalized cover letter
4. **JSON Conversion**: Converts data to JSON format for easy processing
5. **PDF Generation**: Creates professional PDF documents using ReportLab

## Requirements

- Python 3.8+
- OpenAI API key
- See `requirements.txt` for full dependencies

## Example Output

Running JobCraft will generate:
- `resume_CompanyName.pdf` - Customized resume
- `cover_letter_CompanyName.pdf` - Personalized cover letter
- (Optional) `resume.json` and `cover_letter.json` - Intermediate data

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
