from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {"error": "Please upload a PDF file"}

    text_content = ""

    pdf_bytes = await file.read()

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() + "\n"

    return {"content": text_content}

