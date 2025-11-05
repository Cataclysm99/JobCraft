"""
PDF generation utilities for resume and cover letter output.
"""

from typing import Dict, Any
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class PDFGenerator:
    """Generate PDF documents from resume and cover letter data."""
    
    def __init__(self):
        """Initialize PDF generator with styles."""
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor='#34495E',
            spaceAfter=6,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
    
    def generate_resume_pdf(self, resume_dict: Dict[str, Any], output_path: str):
        """
        Generate a PDF resume from resume dictionary.
        
        Args:
            resume_dict: Resume data as dictionary
            output_path: Path to save the PDF
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Name
        name = resume_dict.get("name", "Resume")
        story.append(Paragraph(name, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        # Contact info
        contact = resume_dict.get("contact", {})
        contact_parts = []
        if contact.get("email"):
            contact_parts.append(contact["email"])
        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("location"):
            contact_parts.append(contact["location"])
        
        if contact_parts:
            contact_str = " | ".join(contact_parts)
            story.append(Paragraph(contact_str, self.styles['Contact']))
        
        # LinkedIn and GitHub
        links = []
        if contact.get("linkedin"):
            links.append(f"LinkedIn: {contact['linkedin']}")
        if contact.get("github"):
            links.append(f"GitHub: {contact['github']}")
        if links:
            story.append(Paragraph(" | ".join(links), self.styles['Contact']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        if resume_dict.get("summary"):
            story.append(Paragraph("Professional Summary", self.styles['CustomHeading']))
            story.append(Paragraph(resume_dict["summary"], self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        # Experience
        if resume_dict.get("experience"):
            story.append(Paragraph("Experience", self.styles['CustomHeading']))
            for exp in resume_dict["experience"]:
                story.append(Paragraph(f"• {exp}", self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        # Education
        if resume_dict.get("education"):
            story.append(Paragraph("Education", self.styles['CustomHeading']))
            for edu in resume_dict["education"]:
                story.append(Paragraph(f"• {edu}", self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        # Skills
        if resume_dict.get("skills"):
            story.append(Paragraph("Skills", self.styles['CustomHeading']))
            skills_text = ", ".join(resume_dict["skills"]) if isinstance(resume_dict["skills"], list) else resume_dict["skills"]
            story.append(Paragraph(skills_text, self.styles['BodyText']))
        
        # Build PDF
        doc.build(story)
    
    def generate_cover_letter_pdf(self, cover_letter_dict: Dict[str, Any], output_path: str):
        """
        Generate a PDF cover letter from cover letter dictionary.
        
        Args:
            cover_letter_dict: Cover letter data as dictionary
            output_path: Path to save the PDF
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=1*inch,
            leftMargin=1*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        
        story = []
        
        # Applicant info
        name = cover_letter_dict.get("applicant_name", "")
        email = cover_letter_dict.get("applicant_email", "")
        
        if name:
            story.append(Paragraph(name, self.styles['Normal']))
        if email:
            story.append(Paragraph(email, self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Date and company info
        import datetime
        today = datetime.date.today().strftime("%B %d, %Y")
        story.append(Paragraph(today, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        company = cover_letter_dict.get("company", "Hiring Manager")
        position = cover_letter_dict.get("position", "")
        
        story.append(Paragraph(company, self.styles['Normal']))
        if position:
            story.append(Paragraph(f"Re: {position}", self.styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Cover letter content
        content = cover_letter_dict.get("content", "")
        
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles['BodyText']))
                story.append(Spacer(1, 0.15*inch))
        
        # Build PDF
        doc.build(story)
    
    def generate_combined_pdf(self, resume_dict: Dict[str, Any], 
                            cover_letter_dict: Dict[str, Any], 
                            output_path: str):
        """
        Generate a combined PDF with both resume and cover letter.
        
        Args:
            resume_dict: Resume data as dictionary
            cover_letter_dict: Cover letter data as dictionary
            output_path: Path to save the PDF
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Cover letter first
        self._add_cover_letter_to_story(story, cover_letter_dict)
        
        # Page break
        story.append(PageBreak())
        
        # Resume
        self._add_resume_to_story(story, resume_dict)
        
        # Build PDF
        doc.build(story)
    
    def _add_cover_letter_to_story(self, story, cover_letter_dict):
        """Add cover letter content to story."""
        name = cover_letter_dict.get("applicant_name", "")
        email = cover_letter_dict.get("applicant_email", "")
        
        if name:
            story.append(Paragraph(name, self.styles['Normal']))
        if email:
            story.append(Paragraph(email, self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        import datetime
        today = datetime.date.today().strftime("%B %d, %Y")
        story.append(Paragraph(today, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        company = cover_letter_dict.get("company", "Hiring Manager")
        position = cover_letter_dict.get("position", "")
        
        story.append(Paragraph(company, self.styles['Normal']))
        if position:
            story.append(Paragraph(f"Re: {position}", self.styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        content = cover_letter_dict.get("content", "")
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), self.styles['BodyText']))
                story.append(Spacer(1, 0.15*inch))
    
    def _add_resume_to_story(self, story, resume_dict):
        """Add resume content to story."""
        name = resume_dict.get("name", "Resume")
        story.append(Paragraph(name, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        contact = resume_dict.get("contact", {})
        contact_parts = []
        if contact.get("email"):
            contact_parts.append(contact["email"])
        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("location"):
            contact_parts.append(contact["location"])
        
        if contact_parts:
            contact_str = " | ".join(contact_parts)
            story.append(Paragraph(contact_str, self.styles['Contact']))
        
        links = []
        if contact.get("linkedin"):
            links.append(f"LinkedIn: {contact['linkedin']}")
        if contact.get("github"):
            links.append(f"GitHub: {contact['github']}")
        if links:
            story.append(Paragraph(" | ".join(links), self.styles['Contact']))
        
        story.append(Spacer(1, 0.2*inch))
        
        if resume_dict.get("summary"):
            story.append(Paragraph("Professional Summary", self.styles['CustomHeading']))
            story.append(Paragraph(resume_dict["summary"], self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        if resume_dict.get("experience"):
            story.append(Paragraph("Experience", self.styles['CustomHeading']))
            for exp in resume_dict["experience"]:
                story.append(Paragraph(f"• {exp}", self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        if resume_dict.get("education"):
            story.append(Paragraph("Education", self.styles['CustomHeading']))
            for edu in resume_dict["education"]:
                story.append(Paragraph(f"• {edu}", self.styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))
        
        if resume_dict.get("skills"):
            story.append(Paragraph("Skills", self.styles['CustomHeading']))
            skills_text = ", ".join(resume_dict["skills"]) if isinstance(resume_dict["skills"], list) else resume_dict["skills"]
            story.append(Paragraph(skills_text, self.styles['BodyText']))
