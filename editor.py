import streamlit as st
from parser import * 
import os       
from pathlib import Path                                                                                                                                                                                                 
                                                                                                                                                                    
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
        for img in images:
                    # 3. Saving the Image                                                                                                                                                                                                        
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

            #save_image_to_assets_folder(img.name.split("/")[-1])

        construct_html_content('post.html', post_content, title)
        st.info(f"✅ Story submitted successully `{save_path}`") 



