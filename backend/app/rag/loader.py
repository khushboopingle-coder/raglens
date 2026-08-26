import io
from pypdf import PdfReader
from fastapi import HTTPException

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extract text content from uploaded file bytes (PDF or TXT).
    """
    filename_lower = filename.lower()
    text = ""
    
    if filename_lower.endswith(".pdf"):
        try:
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            extracted_pages = []
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text)
            text = "\n\n".join(extracted_pages)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not extract readable text from PDF document: {str(e)}"
            )
    else:
        # TXT or generic text format
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = file_bytes.decode("latin-1")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to decode text file: {str(e)}"
                )

    clean_text = text.strip()
    if not clean_text:
        raise HTTPException(
            status_code=400,
            detail="Extracted text is empty. Please provide a document containing readable text."
        )
    return clean_text
