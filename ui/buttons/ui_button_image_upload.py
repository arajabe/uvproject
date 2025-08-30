import streamlit as st
from core.model.schema import ParentCreate
from PIL import Image
import pytesseract
import re


def button_upload_image():
    uploaded_file = st.file_uploader("Upload scanned parent form", type=["png", "jpg", "jpeg", "pdf"])
    parsed_data = {}

    if uploaded_file:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)
        st.text_area("Extracted Text", extracted_text, height=200)

        try:
            parsed_data = parse_parent_form(extracted_text)
            for field_name, value in parsed_data.items():
                st.session_state[field_name] = value
        except Exception as e:
            st.warning(f"Could not parse some fields: {e}")

# Generate inputs for all fields
for field_name in ParentCreate.__fields__.keys():
    default_value = st.session_state.get(field_name, "")
    st.session_state[field_name] = st.text_input(field_name.capitalize(), value=default_value)

# Create Pydantic object if we have data
if st.session_state:
    try:
        parent_data = {field_name: st.session_state[field_name] for field_name in ParentCreate.__fields__.keys()}
        parent_obj = ParentCreate(**parent_data)
        st.success("Parent object created successfully!")
        st.json(parent_obj.dict())

        msg_parts = [f"{key}: {value}" for key, value in parent_obj.dict().items()]
        st.text_area("Message Preview", "\n".join(msg_parts), height=200)

    except Exception as e:
        st.error(f"Error: {e}")