from tika import parser

def main():
    parsed = parser.from_file('./dataset/pg74.epub')
    print(parsed["metadata"])
    print(parsed["content"])


if __name__ == "__main__":
    main()
