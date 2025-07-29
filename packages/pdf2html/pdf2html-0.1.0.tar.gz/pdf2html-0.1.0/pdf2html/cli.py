import os
import argparse
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup

def convert_pdf_to_html(pdf_path, output_dir):
    try:
        text = extract_text(pdf_path)
        html = BeautifulSoup("<html><body></body></html>", "html.parser")

        for line in text.split("\n"):
            if line.strip():
                p = html.new_tag("p")
                p.string = line
                html.body.append(p)

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html.prettify())

        print(f"✅ Converted: {pdf_path} → {output_path}")
    except Exception as e:
        print(f"❌ Failed to convert {pdf_path}: {e}")

def convert_all_pdfs_in_folder(folder_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            convert_pdf_to_html(full_path, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF(s) to HTML.")
    parser.add_argument("input", help="Path to PDF file or folder.")
    parser.add_argument("-o", "--output", default="output_html", help="Output folder.")
    args = parser.parse_args()

    input_path = args.input

    if os.path.isfile(input_path) and input_path.lower().endswith(".pdf"):
        convert_pdf_to_html(input_path, args.output)
    elif os.path.isdir(input_path):
        convert_all_pdfs_in_folder(input_path, args.output)
    else:
        print("❌ Error: Please provide a valid PDF file or folder path.")
