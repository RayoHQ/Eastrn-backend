import fitz  # PyMuPDF

def get_page_preview(pdf_path: str, page_number: int):
    try:
        pdf_document = fitz.open(pdf_path)
        if page_number < 1 or page_number > len(pdf_document):
            return {"error": "Invalid page number"}
        page = pdf_document[page_number - 1]
        pix = page.get_pixmap()
        image_data = pix.tobytes("png")  # Return page preview as PNG bytes
        pdf_document.close()
        return {"page": page_number, "preview": image_data}
    except Exception as e:
        return {"error": str(e)}
