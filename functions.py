# functions
from tkinter import *
from PIL import Image, ImageTk

# place an image on the grid
def display_logo(url, row, column):
	img = Image.open(url)
	#resize image
	img = img.resize((int(img.size[0]/1.5), int(img.size[1]/1.5)))
	img = ImageTk.PhotoImage(img)
	img_label = Label(image=img, bg="white")
	img_label.image = img
	img_label.grid(column=column, row=row, rowspan=2, sticky=NW,padx=20, pady=40)

def display_icon(url, row, column, stick, funct):
	icon = Image.open(url)
	#resize image
	icon = icon.resize((20, 20))
	icon = ImageTk.PhotoImage(icon)
	icon_label = Button(image=icon, command=funct, width=25, height=25)
	icon_label.image = icon
	icon_label.grid(column=column, row=row, sticky=stick)


def display_textbox(content, ro, col, root):
	text_box = Text(root, height=10, width=30, padx=10, pady=10)
	text_box.insert(1.0, content)
	text_box.tag_configure("center", justify="center")
	text_box.tag_add("center", 1.0, "end")
	text_box.grid(column=col, row=ro, sticky=SW, padx=25, pady=25)

def extract_images(page):
	images=[]
	if '/XObject' in page['/Resources']:
		xObject = page['/Resources']['/XObject'].get_object()

		for obj in xObject:
			if xObject[obj]['/Subtype'] == '/Image':
				size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
				data = xObject[obj].get_data()
				mode = ""
				if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
					mode = "RGB"
				else:
					mode = "P"

				img = Image.frombytes(mode, size, data)
				images.append(img)
	return images


def display_images(img):
	img = ImageTk.PhotoImage(img)
	img_label = Label(image=img, bg="white")
	img_label.image = img
	img_label.grid(row=4, column=2, rowspan=2)
	return img_label


def resize_image(img):
	width, height = int(img.size[0], int(img.size[1]))
	if width > height:
		height = int(300/width*height)
		width = 300 
	elif height > width:
		width = int(250/height*width)
		height = 250

	else:
		width, height = 250, 250

	img = img.resize((width, height))
	return img


import fitz  # PyMuPDF
import os
from PIL import Image
import io

import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_mupdf(page):
    images = []
    for img in page.get_page_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(page.doc, xref)
        
        # Check if the image uses an alpha channel
        if pix.alpha:
            pix = fitz.Pixmap(fitz.csRGB, pix)  # Convert to RGB

        img_data = pix.tobytes()  # Convert the pixmap to bytes
        img = Image.open(io.BytesIO(img_data))  # Create an Image object

        if img.mode in ["CMYK", "P"]:
            img = img.convert("RGB")  # Convert to RGB if necessary

        images.append(img)
        pix = None  # Clean up pixmap

    return images



