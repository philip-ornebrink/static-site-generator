from textnode import TextNode, TextType
import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def main():
    node = TextNode("hello world", TextType.BOLD, "https://coop.com") 
    print(node)
    source_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/static"
    destination_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/public"
    
    source_to_destination(source_path, destination_path)
    from_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/content"
    template_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/template.html"
    dest_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/public"
    generate_page_recursive(from_path, template_path, dest_path)

def source_to_destination(source_path,destination_path):

    print("src: ", source_path)
    print("dest: ", destination_path)
    if not os.path.exists(source_path):
        raise Exception("Source path does not exists")

    if not os.path.exists(destination_path):
        raise Exception("Destination path does not exists")


    source_dir = os.listdir(source_path)
    for entity in source_dir:
        full_path = os.path.join(source_path, entity)
        if os.path.isfile(full_path):
            print("Copying file to dest: ", entity)
            shutil.copy(full_path, destination_path)
        else:
            print("Copying dir to dest: ", entity)
            dest_dir = os.path.join(destination_path, entity) 
            print("Deleting: ", dest_dir)
            shutil.rmtree(dest_dir, True)
            os.mkdir(dest_dir)
            src_dir = full_path
            source_to_destination(src_dir, dest_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path, "r") as f:
        markdown = f.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    new_template = ""
    with open(template_path, "r") as f:
        template = f.read()
        temp_1 = template.replace("{{ Content }}",content)
        new_template = temp_1.replace("{{ Title }}", title)

    with open(dest_path, "w") as f:
        f.write(new_template)
        



def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")

    print("src: ", dir_path_content)
    print("dest: ", dest_dir_path)
    if not os.path.exists(dir_path_content):
        raise Exception("Source path does not exists")

    if not os.path.exists(dest_dir_path):
        raise Exception("Destination path does not exists")

    content_dir = os.listdir(dir_path_content)
    for entity in content_dir:
        full_path = os.path.join(dir_path_content,entity)
        dest_path = os.path.join(dest_dir_path, entity)
        if entity.find(".md") != -1:
            html_entity = entity.replace(".md", ".html")
            print(f"{entity} to {html_entity}")
            file_path = os.path.join(dest_dir_path, html_entity)
            if os.path.exists(file_path):
                os.remove(file_path)
            print("creating file: ", file_path)
            generate_page(full_path, template_path, file_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(dest_path, True)
            os.mkdir(dest_path)
            generate_page_recursive(full_path, template_path, dest_path)
        else:
            continue






if __name__ == "__main__":
    main()
