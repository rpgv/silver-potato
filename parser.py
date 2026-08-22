import os
import pathlib                                                             
import sys 
import shutil

PATH = pathlib.Path(__file__).parent.resolve()                                                              

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

def construct_html_content(img1, img2, paragraph1, paragraph2):
    img1_name = getattr(img1, "name", img1)
    img2_name = getattr(img2, "name", img2)
    print(img1_name)

    p1 = f"""<div id="development" class="container"><p id='p1' class="p1">{paragraph1}</p></div>"""
    p2 = f"""<div id="development" class="container"><p id='p2' class="p2">{paragraph2}</p></div>"""

    i1 = f"""<div id="image1" class="container"><img src="Images/{img1_name}" alt="no-image-loaded"></div>"""
    i2 = f"""<div id="image2" class="container"><img src="Images/{img2_name}" alt="no-image-loaded"></div>"""

    html_image_01 = i1 if img1_name else ''
    html_image_02 = i2 if img2_name else ''
    html_p_01 = p1 if paragraph1 else ''
    html_p_02 = p2  if paragraph2 else ''

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {box-sizing: border-box;}

        body {
            font-family: sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #FBEFEF;
        }
        /* Remove the problematic grid-template-columns:auto which doesn't work reliably */
        .grid {
            display: flex;        /* Use flex instead of grid for two columns */
        }

        #image01, #introduction {  /* Ensure both main divs are consistent width */
            width: auto;         /* Or set fixed widths like max-width or percentage */
            min-height: 250px;   /* Add minimal height so they align properly */
        }

        /* Make images responsive and remove centering issues with margin:auto on img inside flex children */
        img {
            display: block;       /* Better than position-relative auto-centering in modern browsers */
            max-width: 100%;     /* Ensure it fits containers fully */
            object-fit: cover;   /* Fill container proportionally if needed */}

        body > div:last-child, body > .container:nth-of-type(2) {
            margin-left: auto;   /* Align flex items consistently across both columns */
        }

        .header {
        float: center;
        overflow: hidden;
        background-color: #C5B3D3;
        border-radius: 8px;
        margin-bottom: 5px;
        padding: 20px 10px;
        }
        
        

        .header a {
        float: center;
        color: black;
        text-align: center;
        padding: 12px;
        text-decoration: none;
        font-size: 18px; 
        line-height: 25px;
        border-radius: 4px;
        }

        .logo {
        width: 35px;
        float: left;

        }

        .header a:hover {
        background-color: #ddd;
        color: black;
        }

        @media screen and (max-width: 500px) {
        .header a {
            float: none;
            display: block;
            text-align: left;
        }
        
        .header-right {
            float: none;
        }
        }
        nav ul {
            list-style: none;
            padding: 0;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        nav a {
            color: #000000;
            background-color:#FBEFEF;
            text-decoration: none;
            padding: 10px 15px;
            border: 1px solid #C5B3D3;
            border-radius: 5px;
        }
        .grid {
            grid-template-columns: auto;
        }
        .container {
            display: flex;
            gap: 20px;
            background-color: #FBEFEF;
            padding: 20px;
            margin: 5px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .main-content {
            flex: 3;
        }

        footer {
            display: flex;
            gap: 10px;
            background-color: #C5B3D3;
            padding: 10px;
            margin: 5px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: left;
        }
        .p1 {
            text-align: justify;
            color: #000000;
            flex: 5;
        }
    </style>
</head>
<body>
    <div class="header">
            <a href="#articles">Articles</a>
            <a href="#interviews">Interviews</a>
            <a href="#about">About me</a>
        </div>
        
    </div>
    <div class="grid">"""+html_image_01+html_p_01+""" 
    </div>
"""+html_p_02+html_image_02+"""
    <br>
    <footer>
            <small>For more information contact: </small>
     </footer>
    </body>"""     
    return html

def  overwrite_index_html(html): 
    with open('index.html', 'w') as ov: 
        ov.write(html)
                 
