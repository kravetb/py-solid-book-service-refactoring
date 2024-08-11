import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str):
        self.__title = title
        self.__content = content
    @property
    def title(self) -> str:
        return self.__title

    @property
    def content(self) -> str:
        return self.__content


class Display(ABC):

    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplay(Display):

    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplay(Display):

    def display(self, book: Book) -> None:
        print(book.content[::-1])


class Print(ABC):

    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrint(Print):

    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrint(Print):

    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class Serializer(ABC):

    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JSONSerializer(Serializer):

    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XMLSerializer(Serializer):

    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "console":
                book_display = ConsoleDisplay()
            elif method_type == "reverse":
                book_display = ReverseDisplay()
            else:
                raise ValueError(f"Unknown display type: {method_type}")
            book_display.display(book)
        elif cmd == "print":
            if method_type == "console":
                book_print = ConsolePrint()
            elif method_type == "reverse":
                book_print = ReversePrint()
            else:
                raise ValueError(f"Unknown print type: {method_type}")
            book_print.print_book(book)
        elif cmd == "serialize":
            if method_type == "json":
                serialize_book = JSONSerializer()
            elif method_type == "xml":
                serialize_book = XMLSerializer()
            else:
                raise ValueError(f"Unknown serialize type: {method_type}")
            return serialize_book.serialize(book)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
