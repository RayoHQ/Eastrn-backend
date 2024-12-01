import fitz  # PyMuPDF

from app.core.logger import log_excution_time
from app.core.config import get_settings

class KEYWORDService:
    def __init__(self):
        self.settings = get_settings()

    @log_excution_time
    async def run_keyword_process(self, pdf_path: str, keyword: str):

        print(f"파일 !! : {pdf_path}")

        """
        Search for a keyword in the specified PDF and return page numbers with snippets.

        Args:
            pdf_path (str): Path to the PDF file.
            keyword (str): Keyword to search for.

        Returns:
            list: A list of dictionaries containing page numbers and text snippets where the keyword was found.
        """
        results = []
        keyword_lower = keyword.lower()  # Prepare the keyword for case-insensitive matching
        
        try:
            # Open the PDF using a context manager to ensure proper resource handling
            with fitz.open(pdf_path) as pdf_document:
                # Iterate through each page of the PDF
                for page_number in range(len(pdf_document)):
                    page = pdf_document[page_number]

                    # Extract plain text from the page
                    text = page.get_text("text") or ""  # Safeguard against empty text

                    if keyword_lower in text.lower():
                        # Find all keyword occurrences and their coordinates
                        matches = page.search_for(keyword)

                        for rect in matches:
                            # Extract a snippet of text near the match
                            snippet_index = text.lower().find(keyword_lower)
                            snippet = text[max(0, snippet_index - 50):snippet_index + len(keyword) + 50]

                            # Add match details to the results
                            results.append({
                                "page": page_number + 1,  # Page numbers start from 1
                                "text_snippet": snippet.strip(),
                                "coordinates": {
                                    "x0": rect.x0,
                                    "y0": rect.y0,
                                    "x1": rect.x1,
                                    "y1": rect.y1,
                                },
                            })
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return results
