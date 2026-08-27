import streamlit as st
from template import Template
from pathlib import Path
import parser

template = Template(Path('./index.html'))
template.parse_template()

st.title("Silver-Potato page editor")

with st.form("page_form"):

    # Define image inputs
    images = []
    id = 0
    for i in template.images:
        id = st.file_uploader(f"Upload iamge {id+1}", type=["jpg", "jpeg", "png"])
        images.append(id)

    # Define paragraph inputs
    paragraphs = []
    id = 0
    for i in template.images:
        id = st.text_area(f"Paragraph section {id+1}", max_chars=900, help="Enter your description here")
        paragraphs.append(id)

    # Every form must have a submit button.
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # Parse the inputs (images and descriptions)
        for i in images:
            parser.save_image_to_assets_folder(i)

        # Overwrite index.html
        html = parser.construct_html_content(images, paragraphs, template)
        parser.overwrite_index_html(html)

