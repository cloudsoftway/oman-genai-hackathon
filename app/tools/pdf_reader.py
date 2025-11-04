from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import PyPDF2

##TODO: add hyperlink extraction functionality
class PDFReaderToolInput(BaseModel):
    """Input schema for PDFReaderTool."""
    file_path: str = Field(..., description="The path to the PDF file to read")


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = (
        "Reads and extracts text content from PDF files. "
        "Provide the file path to the PDF document."
    )
    args_schema: Type[BaseModel] = PDFReaderToolInput

    def _run(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if not text.strip():
                    return "Error: Could not extract text from PDF. The file might be empty or image-based."
                
                return text.strip()
        except FileNotFoundError:
            return f"Error: File not found at path: {file_path}"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"


