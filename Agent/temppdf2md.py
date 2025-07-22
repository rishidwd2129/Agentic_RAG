import os
import requests
import pdfplumber
from urllib.parse import urlparse

def _convert_single_pdf(pdf_path: str, output_md_path: str):
    """
    Core function to convert a single PDF file to a Markdown file.

    Args:
        pdf_path (str): The full path to the source PDF file.
        output_md_path (str): The full path for the destination Markdown file.
    """
    try:
        print(f"Processing '{os.path.basename(pdf_path)}' -> '{os.path.basename(output_md_path)}'")
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_md_path), exist_ok=True)

        markdown_content_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            if total_pages == 0:
                print(f"Warning: '{os.path.basename(pdf_path)}' has no pages.")
                return # Skip creating a file for an empty PDF

            for i, page in enumerate(pdf.pages):
                page_number = i + 1
                text = page.extract_text()
                if text:
                    markdown_content_parts.append(f"\n## Page {page_number}\n\n")
                    markdown_content_parts.append(text.strip())
                    markdown_content_parts.append("\n\n---\n\n")
                else:
                    markdown_content_parts.append(f"\n## Page {page_number} (No text found)\n\n---\n\n")

        with open(output_md_path, "w", encoding="utf-8") as md_file:
            md_file.write("".join(markdown_content_parts))
        
        print(f" Successfully converted: {output_md_path}")

    except pdfplumber.PDFSyntaxError as e:
        print(f" Error processing '{os.path.basename(pdf_path)}': {e}. The file might be corrupted.")
    except Exception as e:
        print(f" An unexpected error occurred while processing '{os.path.basename(pdf_path)}': {e}")


def process_pdf_source(
    source_path_or_url: str, 
    output_dir: str, 
    temp_download_dir: str = "Data/Uploads"
):
    """
    Processes a PDF source, which can be a URL, a single file path, or a directory path.

    - If the source is a URL, it's downloaded and converted.
    - If the source is a directory, all PDFs within it are converted.
    - If the source is a single file, it is converted.

    Args:
        source_path_or_url (str): The URL, local file path, or directory path.
        output_dir (str): The directory where Markdown files will be saved.
        temp_download_dir (str): The folder to temporarily store downloaded PDFs.
    """
    # --- 1. Handle URL Source ---
    if source_path_or_url.lower().startswith(('http://', 'https://')):
        print(f"Source is a URL. Attempting to download from: {source_path_or_url}")
        downloaded_pdf_path = None
        try:
            os.makedirs(temp_download_dir, exist_ok=True)
            response = requests.get(source_path_or_url, stream=True)
            response.raise_for_status()

            parsed_url = urlparse(source_path_or_url)
            filename = os.path.basename(parsed_url.path) or "downloaded_file.pdf"
            
            downloaded_pdf_path = os.path.join(temp_download_dir, filename)
            
            print(f"Downloading PDF to: {downloaded_pdf_path}")
            with open(downloaded_pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download complete.")

            output_md_filename = os.path.splitext(filename)[0] + ".md"
            output_md_path = os.path.join(output_dir, output_md_filename)
            _convert_single_pdf(downloaded_pdf_path, output_md_path)

        except requests.exceptions.RequestException as e:
            print(f" Error downloading PDF: {e}")
        finally:
            if downloaded_pdf_path and os.path.exists(downloaded_pdf_path):
                os.remove(downloaded_pdf_path)
                print(f"Cleaned up downloaded file: {downloaded_pdf_path}")
    
    # --- 2. Handle Directory Source ---
    elif os.path.isdir(source_path_or_url):
        print(f"Source is a directory. Processing all PDFs in: {source_path_or_url}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the starting count based on existing files in the output directory
        try:
            existing_files = os.listdir(output_dir)
            start_count = len(existing_files)
            print(f"Output directory '{output_dir}' already contains {start_count} files. New files will be numbered accordingly.")
        except FileNotFoundError:
            start_count = 0

        pdf_files = [f for f in os.listdir(source_path_or_url) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in directory '{source_path_or_url}'.")
            return

        print(f"Found {len(pdf_files)} PDF(s) to convert.")
        for i, filename in enumerate(pdf_files):
            input_pdf_path = os.path.join(source_path_or_url, filename)
            
            # Name files sequentially
            output_md_filename = f"document{start_count + i + 1}.md"
            output_md_path = os.path.join(output_dir, output_md_filename)
            
            _convert_single_pdf(input_pdf_path, output_md_path)

    # --- 3. Handle Single File Source ---
    elif os.path.isfile(source_path_or_url):
        print(f"Source is a single file: {source_path_or_url}")
        if source_path_or_url.lower().endswith('.pdf'):
            filename = os.path.basename(source_path_or_url)
            output_md_filename = os.path.splitext(filename)[0] + ".md"
            output_md_path = os.path.join(output_dir, output_md_filename)
            _convert_single_pdf(source_path_or_url, output_md_path)
        else:
            print(f" Error: File '{source_path_or_url}' is not a PDF.")

    else:
        print(f" Error: The source '{source_path_or_url}' is not a valid URL, file, or directory.")


# --- Example Usage ---
if __name__ == "__main__":
    # Define directories
    INPUT_PDF_DIR = "Data/Upload"
    OUTPUT_MD_DIR = "Data/Markdown_Docs"
    
    # # Create a dummy input directory and a dummy PDF for the example
    # os.makedirs(INPUT_PDF_DIR, exist_ok=True)
    # dummy_pdf_path_1 = os.path.join(INPUT_PDF_DIR, "local_book_1.pdf")
    # dummy_pdf_path_2 = os.path.join(INPUT_PDF_DIR, "local_book_2.pdf")
    # if not os.path.exists(dummy_pdf_path_1):
    #     # NOTE: This creates a text file with a .pdf extension for demonstration.
    #     # For a real test, place actual PDF files in the 'Data/Books' directory.
    #     with open(dummy_pdf_path_1, 'w') as f: f.write("dummy content 1")
    # if not os.path.exists(dummy_pdf_path_2):
    #     with open(dummy_pdf_path_2, 'w') as f: f.write("dummy content 2")


    # --- Example 1: Process a whole directory of PDFs ---
    print("--- Running Directory Example ---")
    process_pdf_source(INPUT_PDF_DIR, OUTPUT_MD_DIR)
    print("\n" + "="*50 + "\n")

    # --- Example 2: Process a PDF from a URL ---
    # print("--- Running URL Example ---")
    # pdf_link = "https://almabooks.com/wp-content/uploads/2020/04/Alice-extract.pdf"
    # process_pdf_source(pdf_link, OUTPUT_MD_DIR)
    # print("\n" + "="*50 + "\n")

    # --- Example 3: Process a single local PDF file ---
    # print("--- Running Single File Example ---")
    # process_pdf_source(dummy_pdf_path_1, OUTPUT_MD_DIR)
    # print("\n" + "="*50 + "\n")
