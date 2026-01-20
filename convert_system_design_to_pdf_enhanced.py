#!/usr/bin/env python3
"""
Enhanced PDF converter for SYSTEM_DESIGN.md with proper ASCII diagram preservation
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Table, TableStyle, Preformatted, KeepTogether, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.colors import HexColor

def create_enhanced_styles():
    """Create enhanced styles for better PDF formatting."""
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=30,
        spaceBefore=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=32
    )
    
    # H1 style (major sections)
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=25,
        fontName='Helvetica-Bold',
        leading=24,
        borderWidth=1,
        borderColor=HexColor('#e0e0e0'),
        borderPadding=8,
        backColor=HexColor('#f8f9fa')
    )
    
    # H2 style (subsections)
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=18,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    # H3 style
    h3_style = ParagraphStyle(
        'H3Style',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=14,
        fontName='Helvetica-Bold',
        leading=16
    )
    
    # Body text
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#2c3e50'),
        spaceAfter=8,
        leading=16,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    )
    
    # Code/Diagram style - smaller font to fit more content
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=6.5,
        textColor=HexColor('#2c3e50'),
        fontName='Courier',
        leftIndent=15,
        rightIndent=15,
        spaceAfter=12,
        spaceBefore=8,
        leading=8,
        backColor=HexColor('#f5f5f5'),
        borderWidth=1,
        borderColor=HexColor('#d0d0d0'),
        borderPadding=10
    )
    
    # List style
    list_style = ParagraphStyle(
        'ListStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#2c3e50'),
        spaceAfter=5,
        leftIndent=25,
        rightIndent=0,
        leading=16,
        bulletIndent=12
    )
    
    # Table of contents style
    toc_style = ParagraphStyle(
        'TOCStyle',
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
        'list': list_style,
        'toc': toc_style
    }

def clean_text(text):
    """Clean text for PDF - remove emojis but keep important symbols."""
    # Keep common symbols but remove emojis
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII except diagrams
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def preserve_ascii_diagrams(text):
    """Check if text looks like an ASCII diagram."""
    # Look for box-drawing characters or patterns that indicate diagrams
    diagram_indicators = [
        '┌', '┐', '└', '┘', '├', '┤', '┬', '┴', '│', '─',
        '═', '║', '╔', '╗', '╚', '╝', '+', '|', '-'
    ]
    return any(char in text for char in diagram_indicators)

def parse_markdown_enhanced(md_content, styles):
    """Enhanced markdown parser with better diagram handling."""
    elements = []
    lines = md_content.split('\n')
    
    i = 0
    in_code_block = False
    code_block = []
    skip_empty = False
    
    while i < len(lines):
        line = lines[i]
        original_line = line
        stripped = line.strip()
        
        # Check for code block markers
        if stripped.startswith('```'):
            if in_code_block:
                # End code block
                if code_block:
                    code_content = '\n'.join(code_block)
                    # Check if it's an ASCII diagram
                    if preserve_ascii_diagrams(code_content) or len(code_block) > 10:
                        # Use Preformatted with smaller font for diagrams
                        preformatted = Preformatted(
                            code_content,
                            style=styles['code'],
                            maxLineLength=120
                        )
                        elements.append(KeepTogether(preformatted))
                        elements.append(Spacer(1, 0.15*inch))
                    else:
                        # Regular code block
                        para = Paragraph(f"<font name='Courier' size='9'>{clean_text(code_content)}</font>", styles['body'])
                        elements.append(para)
                        elements.append(Spacer(1, 0.1*inch))
                code_block = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block.append(line)
            i += 1
            continue
        
        # Main title (# at start)
        if line.startswith('# ') and not line.startswith('##'):
            text = line[2:].strip()
            # Remove table of contents markers
            if '[System Overview]' in text or text.startswith('Table of Contents'):
                i += 1
                continue
            text = clean_text(text)
            elements.append(PageBreak() if elements else Spacer(1, 0))
            elements.append(Paragraph(text, styles['title']))
            elements.append(Spacer(1, 0.3*inch))
        
        # H1 (##)
        elif line.startswith('## ') and not line.startswith('###'):
            text = line[3:].strip()
            if text.startswith('Table of Contents'):
                i += 1
                continue
            text = clean_text(text)
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(text, styles['h1']))
            elements.append(Spacer(1, 0.1*inch))
        
        # H2 (###)
        elif line.startswith('### '):
            text = line[4:].strip()
            text = clean_text(text)
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph(text, styles['h2']))
            elements.append(Spacer(1, 0.08*inch))
        
        # H3 (####)
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = clean_text(text)
            elements.append(Paragraph(text, styles['h3']))
            elements.append(Spacer(1, 0.05*inch))
        
        # Horizontal rule
        elif stripped == '---':
            elements.append(Spacer(1, 0.2*inch))
        
        # Bullet lists (- or *)
        elif stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:].strip()
            # Format bold text
            text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
            # Format inline code
            text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', text)
            text = clean_text(text)
            para = Paragraph(f"• {text}", styles['list'])
            elements.append(para)
        
        # Numbered lists
        elif re.match(r'^\d+\.\s+', stripped):
            match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
            if match:
                num, text = match.groups()
                text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
                text = clean_text(text)
                para = Paragraph(f"{num}. {text}", styles['list'])
                elements.append(para)
        
        # Table of contents links (skip for now)
        elif '[' in stripped and '](' in stripped:
            # Skip TOC entries
            pass
        
        # Empty line
        elif not stripped:
            if not skip_empty:
                elements.append(Spacer(1, 0.05*inch))
                skip_empty = True
            else:
                skip_empty = False
        
        # Regular text
        else:
            skip_empty = False
            if stripped:
                # Format bold
                text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', stripped)
                # Format inline code
                text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', text)
                # Check if it's an ASCII diagram (even outside code blocks)
                if preserve_ascii_diagrams(text) and len(text) > 50:
                    # Treat as diagram
                    preformatted = Preformatted(
                        text,
                        style=styles['code'],
                        maxLineLength=120
                    )
                    elements.append(KeepTogether(preformatted))
                    elements.append(Spacer(1, 0.1*inch))
                else:
                    text = clean_text(text)
                    if text and len(text.strip()) > 2:
                        para = Paragraph(text, styles['body'])
                        elements.append(para)
        
        i += 1
    
    # Handle any remaining code block
    if in_code_block and code_block:
        code_content = '\n'.join(code_block)
        preformatted = Preformatted(
            code_content,
            style=styles['code'],
            maxLineLength=120
        )
        elements.append(KeepTogether(preformatted))
    
    return elements

def create_pdf_enhanced(md_file: str, pdf_file: str):
    """Create enhanced PDF from markdown file."""
    print(f"📄 Converting {md_file} to PDF with enhanced formatting...")
    
    # Create styles
    styles = create_enhanced_styles()
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF document with better margins
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=0.7*inch,
        leftMargin=0.7*inch,
        topMargin=0.8*inch,
        bottomMargin=0.7*inch,
        title="Resource Allocator - System Design",
        author="Resource Allocator Development Team",
        subject="System Architecture and Design Documentation"
    )
    
    # Parse markdown
    elements = parse_markdown_enhanced(md_content, styles)
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"✅ PDF created successfully: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    base_path = Path(__file__).parent
    md_file = base_path / "SYSTEM_DESIGN.md"
    pdf_file = base_path / "SYSTEM_DESIGN.pdf"
    
    if not md_file.exists():
        print(f"❌ Error: {md_file} not found!")
        return
    
    print("🚀 Converting System Design Document to Enhanced PDF...")
    print(f"   Input: {md_file}")
    print(f"   Output: {pdf_file}")
    print()
    
    success = create_pdf_enhanced(str(md_file), str(pdf_file))
    
    if success:
        print()
        print("✅ Conversion complete!")
        print(f"📄 PDF saved: {pdf_file}")
        size_kb = pdf_file.stat().st_size / 1024
        print(f"📊 File size: {size_kb:.1f} KB")
        print()
        print("✨ Features:")
        print("   • All ASCII diagrams preserved")
        print("   • Enhanced formatting and styling")
        print("   • Proper code block handling")
        print("   • Organized sections with headers")
        print("   • Optimized for readability")

if __name__ == "__main__":
    main()
