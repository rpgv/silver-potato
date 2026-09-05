import os
import pathlib                                                             
import sys 
import shutil

PATH = pathlib.Path(__file__).parent.resolve()                                                          
PATTERN_IMG = r'<img> src="(.*?)"</img>'
PATTERN_P = r'<p>"(.*?)"</p>'

def save_image_to_assets_folder(filepath):
    """
    Method to load image into correct folder
    """
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
    """
    Parsing incoming data to rewrite the template html
    """
    with open(pathlib.Path('./index.html'), 'r', -1, 'uft-8') as op:
        html = op.read()
    # Replace images
    i = 0
    for img in images:
        if i:
            old_image = getattr(template.images[img], "name", template.images[img])
            new_image_name = getattr(img, "name", img)
            html = html.replace(old_image, new_image_name)
            i+=1

    # Replace paragraphs
    i = 0
    for p in paragraphs:
        if i:
            old_paragraph_content = template.paragraphs[i].text
            html = html.replace(old_paragraph_content, p)
            i+=1
    return html

def  overwrite_index_html(html):
    """
    Method that overwrites existing html with new one
    """
    with open('index.html', 'w', -1, 'uft-8') as ov:
        ov.write(html)
    return None