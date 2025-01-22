from textnode import TextNode, TextType

def main():
    node = TextNode("hello world", TextType.BOLD_TEXT, "https://coop.com") 
    print(node)


if __name__ == "__main__":
    main()
