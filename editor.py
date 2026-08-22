import streamlit as st

st.title("Silver-Potato page editor")

with st.form("page_form"):
    # First image input
    image1 = st.file_uploader("Upload first image", type=["jpg", "jpeg", "png"])

    # First text box with 300 character limit
    p1 = st.text_area("Description 1 (max 300 characters)", max_chars=300, help="Enter your description here")

    # Second image input
    image2 = st.file_uploader("Upload second image", type=["jpg", "jpeg", "png"])

    # Second text box with 1000 character limit
    p2 = st.text_area("Description 2 (max 1000 characters)", max_chars=1000, help="Enter your description here")

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

