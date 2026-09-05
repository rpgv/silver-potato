import pathlib                                                             
import shutil
import re
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup as bs

PATH = pathlib.Path(__file__).parent.resolve()                                                          
PATTERN_IMG   = r'<img> src="(.*?)"</img>'
PATTERN_IMG_C = r'IMG "(.*?)"'
PATTERN_CONTENT = r'<!-- Begin post -->"(.*?)"<!-- End post -->'


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

    dst_dir = PATH / "Posts"
    dst_dir.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(dst_dir / f'{title}.html')

    md = MarkdownIt("gfm-like2", {"maxNesting": 99})

    images_in_content = re.findall(PATTERN_IMG, content)

    img_n = 0
    if images_in_content:
        for img in images_in_content:
            content = content.replace(img, f'![image_not_loaded](/Images/A{img_n}.png)')
            img_n += 1
    print("Finshed images ... ")

    # Define new <article> content 
    new_content = md.render(content)

    # Load original file 
    with open(template, 'r', -1, 'utf-8') as op:
        template_file = op.read()

    # Parse old content with bs4 
    soup = bs(template_file, 'html5lib')
    old_content = soup.find('article')

    # Create new content object using bs4 
    new_content_object = soup.new_tag('article')
    new_content_object.append(new_content)

    # Replace with regexe old content with new content.
    try:
        old_content.replace_with(new_content)
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