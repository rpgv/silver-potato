import streamlit as st
from template import Template
from pathlib import Path
import parser

template = Template(Path('./clean-blog/index.html'))
template.parse_template()

st.title("Silver-Potato page editor")

with st.form("page_form"):

    # Define image inputs
    images = []
    id_n = 0
    for i in template.images:
        id_ = st.file_uploader(f"Upload iamge {id_n+1}", type=["jpg", "jpeg", "png"])
        images.append(id)
        id_n += 1

    # Define paragraph inputs
    paragraphs = []
    id_n = 0
    for i in template.images:
        id_ = st.text_area(f"Paragraph section {id_n+1}", max_chars=900, help="Enter your description here")
        paragraphs.append(id)
        id_n += 1

    # Every form must have a submit button.
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # Import parser to process the data
        import parser
        
        # Parse the inputs (images and descriptions)
        parser.save_image_to_assets_folder(image1)
        parser.save_image_to_assets_folder(image2)

        # Overwrite index.html
        html = parser.construct_html_content(image1, image2, p1, p2)
        parser.overwrite_index_html(html)

