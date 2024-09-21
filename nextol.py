# nextol extracts and formats all marks and notes of a specific ebook on the
# ebook reader tolino vision 4 HD. It may also work with other models of the
# tolino product family that use a *.txt file with the same structure to store
# the marks and notes.


# imports
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import re
from os import startfile


# functions
def open_and_split(path: str) -> list:
    """Opening a tolino notebook file and splitting it by the separator line
    returning a list of the items
    """
    # const
    LINE_SEPARATOR: str = "\n-----------------------------------\n"

    # var
    data: str
    data_list: list

    # function
    with open(path, encoding="utf-8-sig") as p:
        data = p.read()
    data_list = data.split(LINE_SEPARATOR)
    # fit pattern of other lines for later formatting:
    data_list[0] = "\n" + data_list[0]
    return data_list


def extract_titles(data: list[str]):
    """Extracting all possible book titles from the list of strings and
    returning them as a set
    """
    # const
    PATTERN = re.compile(r".+? \(.+?, .+?\)")

    # var
    titles: set[str] = set()

    # function
    for line in data:
        match = PATTERN.search(line)
        if match:
            titles.add((match.group(0)))
    return titles


def extract_book(data: list[str], title: str) -> list[str]:
    """Extracting the marks and notes for a specific book with title from
    the list data, which must not be empty
    """
    # const
    PATTERN = re.compile(fr"{title}")

    # function
    return [line for line in data if PATTERN.search(line)]


def format(data: list, title: str) -> str:
    """Formatting marks and notes (strings in a list) by removing date, time,
    default text and unnecessary blank lines and converting back to a
    string
    """
    # const
    MARK: str = r"Markierung\xa0auf Seite"
    NOTE: str = r"Notiz\xa0auf Seite"
    BOOKMARK = re.compile(r"Lesezeichen\xa0auf Seite")
    END: str = " \""
    END_NEW: str = "\""
    MARK_NEW: str = r"S."
    NOTE_NEW: str = r"Notiz S."
    HEADER_TEXT: str = f'Markierungen und Notizen aus "{title}":'
    HEADER_SEPARATOR: str = f'\n{"":-^{len(HEADER_TEXT)}}\n\n\n'  # filling up

    # var
    data_new: list[str]

    # function
    data_new = [
        re.sub(
            END, END_NEW, re.sub(NOTE, NOTE_NEW, re.sub(MARK, MARK_NEW, line))
        ) for line in data if not BOOKMARK.search(line)
    ]
    # remove blank and title/author line at beginning
    # and last and date line at the end of every entry
    # (therefore first separate by new lines then glue together again):
    data_new = ["\n".join(line.split("\n")[2:-2]) for line in data_new]
    # return text with header and separate every element with a blank line:
    return HEADER_TEXT + HEADER_SEPARATOR + "\n\n".join(data_new)


# program
if __name__ == "__main__":
    # var
    root = Tk()
    opened: bool = False
    path: str
    data: list
    quit: bool = False
    titles: set[str]
    book: str | None
    startnew: bool | None
    extracted_text: str
    new_path: str

    # main
    root.withdraw()
    while True:
        if not opened:  # do not ask this for further book requests
            path = askopenfilename(
                    parent=root,
                    title="Open tolino notebook",
                    filetypes=[("Text files", "*.txt")]
                )
            if path:
                data = open_and_split(path)
                opened = True
            else:
                quit = messagebox.askyesno(
                    "Quit nextol?",
                    "You cancelled the dialogue. Do you want to quit (yes) "
                    "or do you want to try again (no)?"
                )
            if quit:
                break
            else:
                continue
        titles = extract_titles(data)
        book = askstring(
            "Title of the book?",
            "Please enter the title of the book which marks and notes you "
            "want to extract!\n\nAvailable books:\n" + "\n".join(titles)
        )
        # TODO: ask for book via dropdown
        if book is None or (book.strip() == ""):
            startnew = messagebox.askyesnocancel(
                "Open new note file?",
                "You either cancelled or entered an empty string. "
                "Do you want to start again and open a new note file (yes), "
                "enter a new book title for the already opened note file "
                "(no) or quit the programme (cancel)?"
            )
            if startnew is None:
                break
            elif startnew:
                opened = False
            continue
        data_extracted = extract_book(data, book)
        if len(data_extracted) == 0:
            messagebox.showerror(
                "Nothing found",
                "Could not extract any marks or notes. There is either no "
                "book with this title or the chosen file is not a correctly "
                "formatted tolino note file. Please try again!"
            )
            opened = False  # if it was the wrong note file, open another one
            continue
        # TODO: add option to export to a nicely formatted TeX-File
        extracted_text = format(data_extracted, book)
        new_path = asksaveasfilename(
            parent=root,
            title="Save notes",
            filetypes=[("Text files", "*.txt")]
        )
        if not new_path.endswith(".txt"):
            new_path += ".txt"
        with open(new_path, "w", encoding="utf8") as n:
            n.write(extracted_text)
        if answer := messagebox.askquestion(
            "Open file?",
            "Do you want to open the new file with the extracted marks "
            "and notes?"
        ) == "yes":
            startfile(new_path, "open")
        if answer := messagebox.askquestion(
            "Extract more notes?",
            "Do you want to extract marks and notes from another book?"
        ) == "no":
            break
