from pdfminer.high_level import extract_text

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded PDF or TXT file."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf"):
        try:
            text = extract_text(uploaded_file)
            return text
        except Exception as e:
            return f"[ERROR] Failed to read PDF: {e}"

    else:
        return ""
