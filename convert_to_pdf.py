"""
Convert markdown files to PDF
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_pdf(md_file: str, pdf_file: str, title: str = "Document"):
    """Convert markdown file to PDF."""
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'tables', 'toc']
    )
    
    # Create full HTML document with styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @top-center {{
                    content: "{title}";
                    font-size: 10pt;
                    color: #666;
                }}
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10pt;
                    color: #666;
                }}
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
            }}
            h1 {{
                color: #1f77b4;
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 10px;
                margin-top: 30px;
                page-break-after: avoid;
            }}
            h2 {{
                color: #1f77b4;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 8px;
                margin-top: 25px;
                page-break-after: avoid;
            }}
            h3 {{
                color: #333;
                margin-top: 20px;
                page-break-after: avoid;
            }}
            h4 {{
                color: #555;
                margin-top: 15px;
                page-break-after: avoid;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                page-break-inside: avoid;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #1f77b4;
                color: white;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            li {{
                margin: 5px 0;
            }}
            blockquote {{
                border-left: 4px solid #1f77b4;
                padding-left: 15px;
                margin: 15px 0;
                color: #666;
                font-style: italic;
            }}
            a {{
                color: #1f77b4;
                text-decoration: none;
            }}
            hr {{
                border: none;
                border-top: 2px solid #e0e0e0;
                margin: 20px 0;
            }}
            .toc {{
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            p {{
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=full_html).write_pdf(pdf_file)
    print(f"✅ Converted {md_file} to {pdf_file}")

if __name__ == "__main__":
    # Convert both files
    base_path = Path(__file__).parent
    
    print("Converting markdown files to PDF...")
    print("=" * 50)
    
    # Convert PROJECT_REPORT.md
    markdown_to_pdf(
        str(base_path / "PROJECT_REPORT.md"),
        str(base_path / "PROJECT_REPORT.pdf"),
        "Resource Allocator - Project Report"
    )
    
    # Convert INTERVIEW_QUESTIONS.md
    markdown_to_pdf(
        str(base_path / "INTERVIEW_QUESTIONS.md"),
        str(base_path / "INTERVIEW_QUESTIONS.pdf"),
        "Resource Allocator - Interview Questions & Answers"
    )
    
    print("=" * 50)
    print("✅ All PDFs generated successfully!")
    print(f"📄 PROJECT_REPORT.pdf")
    print(f"📄 INTERVIEW_QUESTIONS.pdf")
