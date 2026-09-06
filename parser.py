import pathlib                                                             
import shutil
import re
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup as bs

PATH = pathlib.Path(__file__).parent.resolve()                                                          


def save_image_to_assets_folder(filepath):
    """
    Saves an image file path by moving the specified image to the assets folder.

    Args:
        filepath (str): The file path of the image to be saved.
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

def construct_html_content(template, content, title):
    """
    Construct HTML from Markdown
    """
    print("Entering construction ... ")

    dst_dir = PATH
    dst_dir.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(dst_dir / f'post_{str(title).strip().replace(" ", "_")}.html')

    md = MarkdownIt("gfm-like2", {"maxNesting": 99})

    images_in_content = re.findall(r'IMG\s+(.*?)\s+', content)

    print("Images found in content: ", images_in_content)

    img_n = 1
    if images_in_content:
        for img in images_in_content:
            content = content.replace(img, f'![image_not_loaded](/Images/A{img_n}.png)')
            img_n += 1

    # Define new <article> content 
    new_content = md.render(content)
    new_soup = bs(new_content, 'html5lib')

    # Load original file 
    with open(template, 'r', -1, 'utf-8') as op:
        template_file = op.read()

    # Parse old content with bs4 
    soup = bs(template_file, 'html5lib')
    base_div = soup.find('div', id='post-content')

    # Create new content object using bs4 
    new_content_object = soup.new_tag('div', class_='col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1')
    for nc in new_soup.find_all(recursive=False):
        new_content_object.append(nc)

    # Replace with regexe old content with new content.
    try:
        base_div.clear()
        base_div.append(new_content_object)
        overwrite_index_html(soup.prettify(), path)
        print("Finshed replacing ... ")

    except Exception as e: 
        print("Error on parser construct_hmtml_content", e)
        exit()

    return None


def  overwrite_index_html(html, path):
    """
    Method that overwrites existing html with new one
    """
    with open(path, 'w', -1, 'utf-8') as ov:
        ov.write(html)
    return None