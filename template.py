from bs4 import BeautifulSoup as bs

class Template(): 
    def __init__(self, file):
        self.file = file

    def parse_template(self):
        with open(self.file, 'r') as of: 
            template_file = of.read()

        self.soup = bs(template_file, 'html5lib')
        paragraphs = []
        for p in soup.find_all('p'):
            paragraphs.append(p)

        images = []
        for img in soup.find_all('img'):
            images.append(img)

        self.paragraphs = paragraphs
        self.images = images
        
    