import pathlib                                                             
import shutil
import re
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup as bs

PATH = pathlib.Path(__file__).parent.resolve()                                                          
class Parser: 
    def __init__(self, template_file, title, parent = [], child = []):
        self.template = template_file
        self.parent = parent
        self.child = child
        dst_dir = PATH
        dst_dir.mkdir(parents=True, exist_ok=True)
        fname = str(title).strip().replace(" ", "_")
        self.path = pathlib.Path(dst_dir / f'post_{fname}.html')

    def load_original(self):
        with open(self.template, 'r', -1, 'utf-8') as op:
            html = op.read()
        self.soup = bs(html, 'html5lib')

    def convert_images(self, content):
        images_in_content = re.findall(r'IMG\s+(.*?)\s+', content)
        img_n = 1
        if images_in_content:
            for img in images_in_content:
                content = content.replace(img, f'![image_not_loaded](/Images/A{img_n}.png)')
                img_n += 1
        return content

    def make_new_soup(self, content, parse = False):
        if parse:
            md = MarkdownIt("gfm-like2", {"maxNesting": 99})
            content = self.convert_images(content)
        content = md.render(content)
        self.n_soup = bs(content, 'html5lib')

    def  overwrite_html_file(self, new_file = False):
        if new_file:
            # Create a new post_file if new file is true
            path = self.path 
        else: 
            # Overwrite existing file if new_file is False
            path = self.template
        with open(path, 'w', -1, 'utf-8') as ov:
            ov.write(self.soup.prettify())

    def create_new_child(self):
         # Parse old content with bs4 
        new_soup = self.new_soup.find(self.parent[0], id=self.parent[1])
        # Create new content object using bs4 
        new_child_tag = new_soup.new_tag(self.child[0], id=self.child[1])
        for nc in new_soup.find_all(recursive=False):
            new_child_tag.append(nc)
        return new_child_tag

    def make_family(self, new_file = False):
        # Find parent
        name = self.parent[0] 
        id_  = self.parent[1]
        parent = self.soup.find(name, id=id_)
        if not parent:
            return None 
        else: 
            # Clear parent object
            parent.clear()
            # Create child based on input
            new_child = self.create_new_child()
            parent.append(new_child)
            # Overwrite 
            self.overwrite_html_file(self.soup.prettify(), new_file)
            return 'Object overwritten successfully'
