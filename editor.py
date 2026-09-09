import streamlit as st
from parser import * 
import os       
from pathlib import Path
from bs4 import NavigableString      
from datetime import datetime                                                                                                                                                                                        
                                                                                                                                                                    
SAVE_DIRECTORY = "Images" 

st.title("Silver-Potato Post editor")

with st.form("page_form"):

    #Publication title
    title = st.text_area("Publication title (will appear on links and page name)")

    # Define paragraph inputs
    post_content = st.text_area("Your next story here....")

    # Define image inputs
    images = []

    uploaded_files = st.file_uploader(
        "Upload images", accept_multiple_files="directory", type=["jpg", "png"]
    )
    for uploaded_file in uploaded_files:
        images.append(uploaded_file)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        print("Copying images to publication directory")
        if images:
            for img in images:                                                                                                                                                                                                       
                try:                                                                                                                                                                                                                         
                    # Get the file extension (e.g., 'png' from 'image.png')                                                                                                                                                                  
                    file_extension = os.path.splitext(img.name)[1]
                    file_name      = Path(os.path.splitext(img.name)[0]).name
                                                                                                                                                                                                        
                    # Create a unique filename based on the original name                                                                                                                                                                    
                    save_path = os.path.join(SAVE_DIRECTORY, f"{file_name}{file_extension}")                                                                                                                                                                                                                                                                                                                                                                       
                    # Read the file contents into bytes                                                                                                                                                                                      
                    file_bytes = img.read()                                                                                                                                                                                    
                                                                                                                                                                                                                                            
                    # Write the bytes to the specified local path                                                                                                                                                                            
                    with open(save_path, "wb") as f:                                                                                                                                                                                         
                        f.write(file_bytes)                                                                                                                                                               
                                                                                                                                                                                                                                            
                except Exception as e:                                                                                                                                                                                                       
                    st.error(f"An error occurred while saving the file: {e}")  

        # Replace publication information  
        new_post = Parser('post.html', title, ['div', 'parent-post-preview'], ['div', 'child'])
        new_post.load_original()
        content = new_post.convert_images(post_content)
        new_post.make_new_soup(content, True)# True -> we want to parse from MD to HTML 
        new_post.make_family(True) # True -> we want to create a new file 

        # Update index information 
        index = Parser('index.html', title, ['div', 'parent-post-preview'], ['', ''])
        index.load_original()
        reference_index = index.soup
        # Get first post-preview format 
        post_preview = reference_index.find('div', id='post-preview')
        new_post_preview = index.soup.new_tag('div', id='post-preview')
        h2 = new_post_preview.new_tag('h2', class_='post-title')
        h2.insert(0, NavigableString(title))
        h3 = new_post_preview.new_tag('h3', class_='post-subtitle')
        h3.insert(0, NavigableString(title))
        p = new_post_preview.new_tag('p',  class_='post-meta')
        p.insert(0, NavigableString(f'Publicado por Joana Araújo Cardoso {datetime.today()}'))
        index.make_new_soup(index.soup)
        index.overwrite_html_file()
        

        # Replace index
        st.info(f"✅ Story submitted successully") 



