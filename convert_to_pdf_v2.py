"""
Convert markdown files to PDF using reportlab
"""

import markdown2
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from pathlib import Path
import re

def clean_html_for_reportlab(html):
    """Convert HTML to reportlab-friendly format."""
    # Remove HTML tags but keep text
    text = re.sub(r'<[^>]+>', '', html)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    return text

def markdown_to_pdf(md_file: str, pdf_file: str, title: str = "Document"):
    """Convert markdown file to PDF."""
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML first
    html = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=20,
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=10,
        spaceBefore=15,
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        spaceBefore=12,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        backColor=colors.HexColor('#f4f4f4'),
        leftIndent=20,
        rightIndent=20,
    )
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Parse HTML and convert to PDF elements
    lines = html.split('\n')
    in_code_block = False
    code_lines = []
    in_table = False
    table_data = []
    
    for line in lines:
        line = line.strip()
        
        # Handle code blocks
        if '<pre>' in line or '<code>' in line:
            in_code_block = True
            code_lines = []
            continue
        if '</pre>' in line or '</code>' in line:
            if code_lines:
                code_text = '\n'.join(code_lines)
                elements.append(Paragraph(code_text, code_style))
                elements.append(Spacer(1, 0.1*inch))
            in_code_block = False
            code_lines = []
            continue
        if in_code_block:
            code_lines.append(clean_html_for_reportlab(line))
            continue
        
        # Handle headings
        if line.startswith('<h1>'):
            text = clean_html_for_reportlab(line)
            elements.append(Paragraph(text, h1_style))
            continue
        if line.startswith('<h2>'):
            text = clean_html_for_reportlab(line)
            elements.append(Paragraph(text, h2_style))
            continue
        if line.startswith('<h3>'):
            text = clean_html_for_reportlab(line)
            elements.append(Paragraph(text, h3_style))
            continue
        
        # Handle lists
        if line.startswith('<li>'):
            text = clean_html_for_reportlab(line)
            # Add bullet
            text = '• ' + text
            elements.append(Paragraph(text, normal_style))
            continue
        
        # Handle paragraphs
        if line.startswith('<p>') or (line and not line.startswith('<') and not line.startswith('</')):
            text = clean_html_for_reportlab(line)
            if text and len(text) > 10:  # Only add non-empty paragraphs
                elements.append(Paragraph(text, normal_style))
                elements.append(Spacer(1, 0.1*inch))
            continue
        
        # Handle horizontal rules
        if '<hr' in line:
            elements.append(Spacer(1, 0.2*inch))
            continue
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Converted {md_file} to {pdf_file}")

if __name__ == "__main__":
    # Convert both files
    base_path = Path(__file__).parent
    
    print("Converting markdown files to PDF...")
    print("=" * 50)
    
    # Convert PROJECT_REPORT.md
    try:
        markdown_to_pdf(
            str(base_path / "PROJECT_REPORT.md"),
            str(base_path / "PROJECT_REPORT.pdf"),
            "Resource Allocator - Project Report"
        )
    except Exception as e:
        print(f"Error converting PROJECT_REPORT.md: {e}")
    
    # Convert INTERVIEW_QUESTIONS.md
    try:
        markdown_to_pdf(
            str(base_path / "INTERVIEW_QUESTIONS.md"),
            str(base_path / "INTERVIEW_QUESTIONS.pdf"),
            "Resource Allocator - Interview Questions & Answers"
        )
    except Exception as e:
        print(f"Error converting INTERVIEW_QUESTIONS.md: {e}")
    
    print("=" * 50)
    print("✅ PDF generation complete!")
    print(f"📄 Check for PROJECT_REPORT.pdf")
    print(f"📄 Check for INTERVIEW_QUESTIONS.pdf")
