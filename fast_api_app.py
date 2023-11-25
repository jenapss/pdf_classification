from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import utils_jelal
from transformers import LayoutLMv2FeatureExtractor, LayoutLMv2Tokenizer, LayoutLMv2Processor
from PIL import Image
import fitz
import os
from io import BytesIO
#import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' 
app = FastAPI()
feature_extractor = LayoutLMv2FeatureExtractor()
tokenizer = LayoutLMv2Tokenizer.from_pretrained("OCRmodel/")
processor = LayoutLMv2Processor(feature_extractor, tokenizer)
id2label={0: "insurance",
 1: "cc&r",
 2: "rules&regulations",
 3: "by_law",
 4: "plat",
 5: "finances"}



from transformers import LayoutLMv2ForSequenceClassification
import torch
model_dir = "OCRmodel/"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = LayoutLMv2ForSequenceClassification.from_pretrained(model_dir)
model.to(device)
def convert_pdf_to_tiff(pdf_path, tiff_path, max_pixels=178956970, max_size=(2000, 2000), max_pages=3):
    pdf_document = fitz.open(pdf_path)

    # Create a list to store images
    images = []

    # Iterate over the first two or three pages
    for page_number in range(min(pdf_document.page_count, max_pages)):
        # Get the page
        page = pdf_document[page_number]

        # Render the page as an image (RGB)
        pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save each page as a separate TIFF file
        page_tiff_path = tiff_path.replace('.tiff', f'_page{page_number + 1}.tiff')
        img.save(page_tiff_path, format="TIFF")
        images.append(page_tiff_path)

    # Close the PDF document
    pdf_document.close()

    # Combine separate TIFF files into a multi-page TIFF
    first_image = Image.open(images[0])
    rest_of_images = [Image.open(image_path) for image_path in images[1:]]
    
    first_image.save(tiff_path, save_all=True, append_images=rest_of_images)

    # Resize the image if it exceeds the maximum allowed size
    combined_image = Image.open(tiff_path)
    if combined_image.size[0] * combined_image.size[1] > max_pixels:
        combined_image.thumbnail(max_size)
        combined_image.save(tiff_path, format="TIFF")

    # Remove separate TIFF files
    for image_path in images:
        os.remove(image_path)

    return tiff_path


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save the received PDF file
        pdf_path = f"uploads/{file.filename}"
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(file.file.read())

        # Convert PDF to TIFF
        tiff_path = convert_pdf_to_tiff(pdf_path, f"uploads/{file.filename.replace('.pdf', '.tiff')}")

        # Open the TIFF image
        image = Image.open(tiff_path)
        image = image.convert("RGB")

        # Perform classification
        document_class = utils_jelal.classify_docs(image, processor, model)

        return JSONResponse(content={"filename": file.filename, "predicted_label": id2label[document_class]}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up: Delete the original PDF and TIFF files after processing
        os.remove(pdf_path)
        os.remove(tiff_path)

@app.get("/health")
async def health_check():
    return {"status": "OK"}