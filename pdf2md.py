import requests
import pdfplumber
import os
import tempfile

def pdf_to_markdown(pdf_url: str, output_filename: str):
    """
    Converts a PDF file from a direct URL to a Markdown (.md) file.

    This function extracts text content from each page of the PDF and saves it
    into a Markdown file. It adds page number headings and horizontal rules
    to separate pages in the output Markdown.

    Limitations:
    - This conversion is primarily text-based. Images, complex layouts,
      tables, and other non-textual elements in the PDF will not be
      converted or accurately represented in the Markdown file.
    - Formatting (bold, italics, font sizes) from the PDF is generally lost.

    Args:
        pdf_url (str): The direct URL to the PDF file.
        output_filename (str): The name of the output Markdown file (e.g., "output.md").
                               The file will be saved in the current directory.
    """
    print(f"Attempting to convert PDF from: {pdf_url}")
    print(f"Output will be saved to: {os.path.abspath(output_filename)}")

    temp_pdf_path = None
    try:
        # 1. Download the PDF file
        print("Downloading PDF...")
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Create a temporary file to store the downloaded PDF
        # Using tempfile ensures a unique and secure temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_pdf_path = temp_file.name
        print(f"PDF downloaded to temporary file: {temp_pdf_path}")

        # 2. Extract text and format as Markdown
        print("Extracting text from PDF and formatting as Markdown...")
        markdown_content_parts = []
        with pdfplumber.open(temp_pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                page_number = i + 1
                print(f"Processing page {page_number}/{total_pages}...")
                text = page.extract_text()
                if text:
                    # Add a Markdown heading for the page number
                    markdown_content_parts.append(f"\n## Page {page_number}\n\n")
                    markdown_content_parts.append(text)
                    # Add a horizontal rule for visual separation between pages
                    markdown_content_parts.append("\n\n---\n\n")
                else:
                    markdown_content_parts.append(f"\n## Page {page_number} (No text found)\n\n---\n\n")

        # 3. Save the content to a Markdown file
        print(f"Saving extracted content to {output_filename}...")
        # Use utf-8 encoding to handle various characters
        with open(output_filename, "w", encoding="utf-8") as md_file:
            md_file.write("".join(markdown_content_parts))

        print(f"Successfully converted PDF to Markdown: {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        print("Please check the URL and your internet connection.")
    except pdfplumber.PDFSyntaxError as e:
        print(f"Error processing PDF (syntax error): {e}")
        print("The PDF file might be corrupted, encrypted, or malformed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up the temporary PDF file if it was created
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            print(f"Cleaned up temporary PDF file: {temp_pdf_path}")

# --- Example Usage ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual URL of the PDF you want to convert
    pdf_link = "https://almabooks.com/wp-content/uploads/2020/04/Alice-extract.pdf" # Example PDF link
    output_md_file = "Alice_the_Wonder_Land.md"  # Name of the output Markdown file

    pdf_to_markdown(pdf_link, output_md_file)

    # You can uncomment and use the following for another example:
    # pdf_link_2 = "https://arxiv.org/pdf/2407.03450" # Another example PDF
    # output_md_file_2 = "another_paper.md"
    # pdf_to_markdown(pdf_link_2, output_md_file_2)
