import os, bs4
# from .decorators import execution_time
from bs4 import BeautifulSoup


def list_html(exclude_dirs=None, show=True):
    path = os.getcwd()
    extentions = ('html', 'htm')
    if not exclude_dirs:
        exclude_dirs = []
    file_paths = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [i for i in dirs if i not in exclude_dirs]
        for file in files:
            if file.endswith(extentions):
                if show:
                    print(os.path.relpath(os.path.join(root, file), path).replace('\\', '/'))
                else:
                    file_paths.append(os.path.relpath(os.path.join(root, file), path).replace('\\', '/'))

    if not show:
        return file_paths

def render_templates(template_url, target_files, content_id, indent=4):
    formatter = bs4.formatter.HTMLFormatter(indent=indent)
    directory_files ={i.split('/')[-1]: i for i in list_html(show=False)}


    if not os.path.exists(template_url):
        print("Template not found:", template_url)
        return
    with open(template_url, 'r') as f:
        template = f.read()
        template_soup = BeautifulSoup(template, 'html.parser')
        new_content_div = template_soup.find(id=content_id)
        if not new_content_div:
            print('No content section found in template')
            return
        for file_path in target_files:
            if not os.path.exists(file_path):
                print('File not Found:', file_path)
                similar_file = directory_files.get(file_path.split('/')[-1])
                if similar_file:
                    print("There is a similar file in:", similar_file)
                  
                continue
            with open(file_path, 'r') as file:
                target_content = file.read()
            if len(target_content)==0:
                with open(file_path, 'w') as f:
                    f.write(template)
                    print("Blank file template rendered:", file_path)
                    continue
            target_soup = BeautifulSoup(target_content, 'html.parser')

            # Extract content section
            content_div = target_soup.find(id=content_id)
            if not content_div:
                print("No content section found in", file_path)
                continue
            dynamic_content = content_div.decode_contents()
            
            new_content_div.clear()
            new_content_div.append(BeautifulSoup(dynamic_content, 'html.parser'))

            with open(file_path, 'w') as f:
                f.write(str(template_soup.prettify(formatter=formatter)))
            print("File update successfully:", file_path)

