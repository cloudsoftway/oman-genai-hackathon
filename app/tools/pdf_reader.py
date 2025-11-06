from crewai.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import os
import PyPDF2

class PDFReaderToolInput(BaseModel):
    """Input schema for PDFReaderTool."""
    file_path: str = Field(..., description="The path to the PDF file to read")
    output_dir: Optional[str] = Field(None, description="Directory to save the extracted text file")

class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = (
        "Reads and extracts text content from PDF files and also injects hyperlinks found on each page "
        "into the extracted text (at the end of that page)."
    )
    args_schema: Type[BaseModel] = PDFReaderToolInput

    def _extract_links_from_page(self, page: PyPDF2._page.PageObject) -> List[str]:
        """Extract hyperlinks from a single PDF page, if any."""
        links = []
        if "/Annots" in page:
            for annot in page["/Annots"]:
                try:
                    annot_obj = annot.get_object()
                    if "/A" in annot_obj and "/URI" in annot_obj["/A"]:
                        uri = annot_obj["/A"]["/URI"]
                        links.append(uri)
                except Exception:
                    continue
        return links

    def _run(self, file_path: str, output_dir: Optional[str] = None) -> str:
        """
        Extract text from a PDF file. For each page, if hyperlinks are found,
        they are appended right after that page's text. Optionally save to output_dir.
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                full_text_parts = []

                for page_idx, page in enumerate(pdf_reader.pages, start=1):
                    # extract page text
                    page_text = page.extract_text() or ""
                    # extract links for this page
                    page_links = self._extract_links_from_page(page)

                    # build page output
                    page_output = page_text.rstrip()

                    if page_links:
                        # add a small header so we know these links belong to this page
                        links_lines = [f"{i+1}. {link}" for i, link in enumerate(page_links)]
                        page_output += "\n\n[Links on this page]\n" + "\n".join(links_lines)

                    # separate pages clearly
                    full_text_parts.append(page_output)

                full_text = "\n\n--- PAGE BREAK ---\n\n".join(full_text_parts).strip()

                if not full_text:
                    return "Error: Could not extract text from PDF. The file might be empty or image-based."

                # Save extracted text if output_dir is provided
                output_path = None
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    base_name = os.path.basename(file_path)
                    file_name = os.path.splitext(base_name)[0] + ".txt"
                    output_path = os.path.join(output_dir, file_name)
                    with open(output_path, "w", encoding="utf-8") as out_file:
                        out_file.write(full_text)

                if output_path:
                    return f"Text (with page links) extracted and saved to {output_path}"
                else:
                    # if you want to return the whole text instead, change this line
                    return "Successfully extracted text (links added next to their pages)."

        except FileNotFoundError:
            return f"Error: File not found at path: {file_path}"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
