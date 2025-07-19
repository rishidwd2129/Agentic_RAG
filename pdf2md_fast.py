import requests
import pdfplumber
import os
import tempfile
import concurrent.futures # Added for threading

def _process_single_page(page_tuple):
    """
    Helper function to process a single PDF page.
    Takes a tuple (page_number, pdfplumber_page_object).
    Returns a tuple (page_number, formatted_markdown_string_for_page).
    """
    page_number, page = page_tuple
    extracted_text = "" # Initialize with empty string
    try:
        # Attempt to extract text
        text_from_page = page.extract_text()
        if text_from_page is not None:
            extracted_text = text_from_page
        # If text_from_page is None, extracted_text remains an empty string,
        # which will lead to the "No text found" message.
    except Exception as e:
        # Log the specific error if extraction fails for this page
        print(f"Error extracting text from page {page_number}: {type(e).__name__}: {e}")
        # Mark the page content with an error message in the Markdown
        return (page_number, f"\n## Page {page_number} (Error during text extraction: {type(e).__name__}: {e})\n\n---\n\n")

    # If extraction was successful (or returned None), format the content
    if extracted_text:
        return (page_number, f"\n## Page {page_number}\n\n{extracted_text}\n\n---\n\n")
    else:
        return (page_number, f"\n## Page {page_number} (No text found or extracted)\n\n---\n\n")


def pdf_to_markdown_multithreaded(pdf_url: str, output_filename: str, max_workers: int = None):
    """
    Converts a PDF file from a direct URL to a Markdown (.md) file using
    multi-threading for parallel page processing.

    This function downloads the PDF, then extracts text content from each page
    concurrently, and saves it into a Markdown file. It adds page number
    headings and horizontal rules to separate pages in the output Markdown.

    Limitations:
    - This conversion is primarily text-based. Images, complex layouts,
      tables, and other non-textual elements in the PDF will not be
      converted or accurately represented in the Markdown file.
    - Formatting (bold, italics, font sizes) from the PDF is generally lost.

    Args:
        pdf_url (str): The direct URL to the PDF file.
        output_filename (str): The name of the output Markdown file (e.g., "output.md").
                               The file will be saved in the current directory.
        max_workers (int, optional): The maximum number of threads to use for
                                     page processing. If None, a default is chosen
                                     (usually min(32, os.cpu_count() + 4)).
    """
    print(f"Attempting to convert PDF from: {pdf_url}")
    print(f"Output will be saved to: {os.path.abspath(output_filename)}")
    if max_workers:
        print(f"Using a maximum of {max_workers} worker threads for page processing.")
    else:
        print("Using default number of worker threads for page processing.")


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

        # 2. Extract text and format as Markdown using multi-threading
        print("Extracting text from PDF and formatting as Markdown using multi-threading...")

        # Open the PDF once for all threads
        with pdfplumber.open(temp_pdf_path) as pdf:
            total_pages = len(pdf.pages)
            # Prepare a list of (page_number, page_object) tuples for processing
            pages_to_process = [(i + 1, page) for i, page in enumerate(pdf.pages)]

            # Use ThreadPoolExecutor for concurrent page processing
            # The results will be stored in a list, ordered by page number
            # Initialize with None to hold results in correct order
            ordered_markdown_parts = [None] * total_pages

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit each page for processing and map futures to their original page numbers
                future_to_page_num = {executor.submit(_process_single_page, page_data): page_data[0]
                                      for page_data in pages_to_process}

                for future in concurrent.futures.as_completed(future_to_page_num):
                    original_page_num = future_to_page_num[future]
                    try:
                        page_num_returned, markdown_part = future.result()
                        # Place the result in the correct position in the ordered list
                        ordered_markdown_parts[page_num_returned - 1] = markdown_part
                        print(f"Finished processing page {page_num_returned}/{total_pages}")
                    except Exception as exc:
                        print(f"Page {original_page_num} generated an unhandled exception in the main loop: {exc}")
                        # This catch is for exceptions that somehow escape _process_single_page
                        # and are raised when calling future.result()
                        ordered_markdown_parts[original_page_num - 1] = \
                            f"\n## Page {original_page_num} (Critical Error during processing in main loop: {exc})\n\n---\n\n"

        # 3. Join all the ordered markdown parts
        final_markdown_content = "".join(part for part in ordered_markdown_parts if part is not None)

        # 4. Save the content to a Markdown file
        print(f"Saving extracted content to {output_filename}...")
        # Use utf-8 encoding to handle various characters
        with open(output_filename, "w", encoding="utf-8") as md_file:
            md_file.write(final_markdown_content)

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
    # For testing multi-threading, use a PDF with many pages if possible.
    pdf_link = "https://docs.aws.amazon.com/pdfs/lambda/latest/dg/lambda-dg.pdf#getting-started" # Example PDF link
    output_md_file = "AWS_Lamnda_Doc_Multithreaded.md"  # Name of the output Markdown file

    # You can specify max_workers, or leave it as None to use the default.
    # A good starting point for I/O bound tasks is often more than CPU cores,
    # but too many threads can also cause overhead.
    pdf_to_markdown_multithreaded(pdf_link, output_md_file, max_workers=8)

    # You can uncomment and use the following for another example:
    # pdf_link_2 = "https://arxiv.org/pdf/2407.03450" # Another example PDF (often has many pages)
    # output_md_file_2 = "another_paper_multithreaded.md"
    # pdf_to_markdown_multithreaded(pdf_link_2, output_md_file_2)
