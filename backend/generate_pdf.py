import markdown2
from weasyprint import HTML, CSS
from pathlib import Path

# Read the markdown file
md_path = Path(__file__).parent.parent / ".gemini" / "antigravity" / "brain" / "7227e4c7-898f-410e-9afb-b929d9d3c929" / "API_DOCUMENTATION.md"
output_path = Path(__file__).parent / "API_DOCUMENTATION.pdf"

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables'])

# Wrap in a styled HTML document
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            color: #ecf0f1;
        }}
        strong {{
            color: #2980b9;
        }}
        hr {{
            border: none;
            border-top: 1px solid #bdc3c7;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Generate PDF
HTML(string=full_html).write_pdf(output_path)
print(f"PDF generated successfully at: {output_path}")
