import streamlit as st
import cv2
import numpy as np
import pytesseract
import easyocr
from config import LLM_MODEL, LLM_API_KEY
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


def application():

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    

    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Load image from Streamlit file uploader or local path
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding or denoising
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Optional: blur to reduce noise
    gray = cv2.medianBlur(gray, 3)

    # OCR handwritten text
    extracted_text = pytesseract.image_to_string(gray, lang='eng')
    

    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)
    extracted_text = " ".join([r[1] for r in result])

    st.markdown(extracted_text)

    client = ChatGroq(model=LLM_MODEL, temperature=0, api_key=LLM_API_KEY)

    prompt = f"""
    Convert the following handwritten form text into JSON with keys: 
    name, age, father_name, address. 
    Text: {extracted_text}
    """

    response = client.invoke([HumanMessage(content=prompt)])
    

    json_output = response.content
    st.markdown(json_output)



