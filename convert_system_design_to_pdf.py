#!/usr/bin/env python3
"""
Convert SYSTEM_DESIGN.md to a well-organized PDF with proper formatting for ASCII diagrams
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

def setup_fonts():
    """Setup fonts for PDF."""
    try:
        # Try to use built-in fonts
        pdfmetrics.registerFont(pdfmetrics.getFont('Helvetica'))
    except:
        pass

def create_styles():
    """Create custom styles for the PDF."""
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Heading 1 style
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderPadding=0
    )
    
    # Heading 2 style
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )
    
    # Heading 3 style
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('#34495e'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=HexColor('#2c3e50'),
        spaceAfter=6,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # Code/Diagram style
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=7,
        textColor=HexColor('#2c3e50'),
        fontName='Courier',
        leftIndent=10,
        rightIndent=10,
        spaceAfter=10,
        leading=9,
        backColor=HexColor('#f5f5f5')
    )
    
    # List item style
    list_style = ParagraphStyle(
        'CustomList',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=HexColor('#2c3e50'),
        spaceAfter=4,
        leftIndent=20,
        leading=14
    )
    
    return {
        'title': title_style,
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'body': body_style,
        'code': code_style,
        'list': list_style
    }

def escape_html(text):
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def parse_markdown(md_content, styles):
    """Parse markdown content and convert to PDF elements."""
    elements = []
    lines = md_content.split('\n')
    
    i = 0
    in_code_block = False
    code_block = []
    code_block_type = None
    
    while i < len(lines):
        line = lines[i]
        
        # Check for code block start/end
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                code_content = '\n'.join(code_block)
                # Use Preformatted for ASCII diagrams
                preformatted = Preformatted(
                    code_content,
                    style=styles['code'],
                    maxLineLength=100
                )
                elements.append(KeepTogether(preformatted))
                elements.append(Spacer(1, 0.1*inch))
                code_block = []
                in_code_block = False
                code_block_type = None
            else:
                # Start of code block
                in_code_block = True
                code_block_type = line.strip()[3:].strip() or 'text'
            i += 1
            continue
        
        if in_code_block:
            code_block.append(line)
            i += 1
            continue
        
        # Headers
        if line.startswith('# '):
            text = line[2:].strip()
            # Remove emojis for cleaner PDF
            text = re.sub(r'[^\w\s\-().,;:!?]', '', text)
            elements.append(Paragraph(escape_html(text), styles['title']))
            elements.append(Spacer(1, 0.2*inch))
        elif line.startswith('## '):
            text = line[3:].strip()
            text = re.sub(r'[^\w\s\-().,;:!?]', '', text)
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(escape_html(text), styles['h1']))
            elements.append(Spacer(1, 0.1*inch))
        elif line.startswith('### '):
            text = line[4:].strip()
            text = re.sub(r'[^\w\s\-().,;:!?]', '', text)
            elements.append(Paragraph(escape_html(text), styles['h2']))
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = re.sub(r'[^\w\s\-().,;:!?]', '', text)
            elements.append(Paragraph(escape_html(text), styles['h3']))
        # Horizontal rule
        elif line.strip() == '---':
            elements.append(Spacer(1, 0.2*inch))
            # Add a line
            elements.append(Spacer(1, 0.05*inch))
        # Bullet lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:].strip()
            # Remove emojis but keep structure
            text = re.sub(r'^\S+\s+', '', text) if text else text
            # Format as list
            para = Paragraph(f"• {escape_html(text)}", styles['list'])
            elements.append(para)
        # Numbered lists
        elif re.match(r'^\d+\.\s+', line.strip()):
            text = re.sub(r'^\d+\.\s+', '', line.strip())
            text = re.sub(r'^\S+\s+', '', text) if text else text
            para = Paragraph(escape_html(text), styles['list'])
            elements.append(para)
        # Empty line
        elif not line.strip():
            elements.append(Spacer(1, 0.05*inch))
        # Regular text
        else:
            # Clean up emojis and special characters for PDF
            clean_line = line.strip()
            if clean_line:
                # Format bold text
                clean_line = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', clean_line)
                # Format inline code
                clean_line = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', clean_line)
                # Remove remaining emojis
                clean_line = re.sub(r'[^\w\s\-().,;:!?\*`<>/&]', '', clean_line)
                
                para = Paragraph(escape_html(clean_line), styles['body'])
                elements.append(para)
        
        i += 1
    
    # Handle any remaining code block
    if in_code_block and code_block:
        code_content = '\n'.join(code_block)
        preformatted = Preformatted(
            code_content,
            style=styles['code'],
            maxLineLength=100
        )
        elements.append(KeepTogether(preformatted))
    
    return elements

def create_pdf(md_file: str, pdf_file: str):
    """Create PDF from markdown file."""
    print(f"📄 Converting {md_file} to PDF...")
    
    # Setup
    setup_fonts()
    styles = create_styles()
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Parse markdown
    elements = parse_markdown(md_content, styles)
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF created: {pdf_file}")

def main():
    """Main function."""
    base_path = Path(__file__).parent
    md_file = base_path / "SYSTEM_DESIGN.md"
    pdf_file = base_path / "SYSTEM_DESIGN.pdf"
    
    if not md_file.exists():
        print(f"❌ Error: {md_file} not found!")
        return
    
    print("🚀 Converting System Design Document to PDF...")
    print(f"   Input: {md_file}")
    print(f"   Output: {pdf_file}")
    print()
    
    create_pdf(str(md_file), str(pdf_file))
    
    print()
    print("✅ Conversion complete!")
    print(f"📄 PDF saved: {pdf_file}")
    print()
    print(f"📊 File size: {pdf_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
