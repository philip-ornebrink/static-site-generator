from textnode import TextNode, TextType
import os
import shutil

def main():
    node = TextNode("hello world", TextType.BOLD, "https://coop.com") 
    print(node)
    source_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/static"
    destination_path = "/Users/Standard/Desktop/MyCodingProjects/github.com/philip-ornebrink/static-site-generator/public"
    
    source_to_destination(source_path, destination_path)

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
            shutil.rmtree(dest_dir, True)
            os.mkdir(dest_dir)
            src_dir = full_path
            source_to_destination(src_dir, dest_dir)


if __name__ == "__main__":
    main()
