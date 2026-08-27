import os
import pathlib                                                             
from bs4 import BeautifulSoup as bs
import re
import shutil

PATH = pathlib.Path(__file__).parent.resolve()                                                          
PATTERN_IMG = r'<img> src="(.*?)"</img>'                                                             

def save_image_to_assets_folder(filepath):
    if not filepath:
        return
    try:
        dst_dir = PATH / "Images"
        dst_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if filepath is a Streamlit UploadedFile or file-like object
        if hasattr(filepath, "name") and not isinstance(filepath, (str, pathlib.Path)):
            fname = filepath.name
            with open(dst_dir / fname, "wb") as f:
                f.write(filepath.getbuffer())
        else:
            src_path = pathlib.Path(filepath)
            fname = src_path.name
            shutil.copy2(src_path, dst_dir / fname)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print("An unexpected error occurred: " + str(e))

def construct_html_content(images, paragraphs, template):
    with open(pathlib.Path('./index.html'), 'r') as op:
        html = op.read()
    # Replace images
    i = 0
    for i in template.images:
        if i:
            new_img_name = getattr(i, "name", i)
            img_match = re.sub(PATTERN_IMG, new_img_name, template.images[i])
            html = html.replace(img_match, new_img_name)
            i+=1

    # Replace paragraphs
    i = 0
    for p in template.paragraphs:
        if p.text:
            

    
    return html

def  overwrite_index_html(html): 
    with open('index.html', 'w') as ov: 
        ov.write(html)
                 
