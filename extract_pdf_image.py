import fitz  # PyMuPDF
import os
from PIL import Image
import io

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    # print(doc)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image_filename = f"papers/images/image_{os.path.basename(pdf_path).split('.')[0]}_page_{i}_{xref}.{image_ext}"
            image.save(image_filename)
    doc.close()

def extract_images_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            extract_images_from_pdf(pdf_path)
            print(f"Extracted images from {filename}")

# Specify your folder path here
folder_path = 'papers/'
extract_images_from_folder(folder_path)
