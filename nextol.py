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
def open_and_split() -> list:
    """Opening a tolino notebook file and splitting it by the separator line
    returning a list of the items
    """
    # const
    LINE_SEPARATOR: str = "\n-----------------------------------\n"

    # var
    path: str
    data: str
    data_list: list

    # function
    path = askopenfilename(
        parent=root,
        title="Open tolino notebook",
        filetypes=[("Text files", "*.txt")]
    )
    # TODO: If you abort this, there currently will be a FileNotFoundError...
    with open(path, encoding="utf-8-sig") as p:
        data = p.read()
    data_list = data.split(LINE_SEPARATOR)
    data_list[0] = "\n" + data_list[0]  # fit the pattern of the other lines
    return data_list


def extract(data: list, title: str) -> list:
    """Extracting the marks and notes for a specific book with title from
    the list data, which must not be empty
    """
    # var
    data_res = data.copy()
    pattern = fr"{title}"
    x: int = 0

    # function
    while x < len(data_res):
        if not re.search(pattern, data_res[x]):
            data_res.pop(x)
        else:
            x += 1
    return data_res


def format(data: list, title: str) -> str:
    """Formatting marks and notes (strings in a list) by removing date, time,
    default text and unnecessary blank lines and converting back to a
    string
    """
    # const
    MARK: str = r"Markierung\xa0auf Seite"
    NOTE: str = r"Notiz\xa0auf Seite"
    BOOKMARK: str = r"Lesezeichen\xa0auf Seite"
    MARK_NEW: str = r"S."
    NOTE_NEW: str = r"Notiz S."
    HEADER_TEXT: str = f'Markierungen und Notizen aus "{title}":'
    HEADER_SEPARATOR: str = f'\n{"":-^{len(HEADER_TEXT)}}\n\n\n'  # filling up

    # var
    new_data: list = []
    temp_data: list
    text: str
    x: int = 0

    # function
    while x < len(data):
        # len(data) must be bigger than 0 (assured through the main program)
        if re.search(BOOKMARK, data[x]):
            data.pop(x)  # removing bookmarks (they do not give information)
        else:
            # replacing long site info with short one:
            data[x] = re.sub(MARK, MARK_NEW, data[x])
            data[x] = re.sub(NOTE, NOTE_NEW, data[x])
            temp_data = data[x].split("\n")
            for i in range(2):
                temp_data.pop(0)  # remove blank and title/author line
                temp_data.pop(len(temp_data)-1)  # remove last and date line
            new_data.append("\n".join(temp_data))
            x += 1

    text = HEADER_TEXT + HEADER_SEPARATOR  # starting new file with header
    for dat in new_data:
        text += dat + "\n\n"  # separating marks/notes with blank lines
    return text


# program
if __name__ == "__main__":
    # var
    root = Tk()
    data: list
    opened: bool = False
    book: str | None
    extracted_text: str
    new_path: str

    # main
    root.withdraw()
    while True:
        if not opened:  # do not ask this for further book requests
            data = open_and_split()
            opened = True
        # TODO: scan data for available books and ask for book via dropdown
        book = askstring(
            "Title of the book?",
            "Please enter the title of the book which marks and notes you "
            "want to extract!")
        # TODO: This currently only works if there is only one book with the 
        # same title. If there are two books with the same title or the user 
        # given title could be part of another book title search for the title 
        # with the author like this: "TITLE \(AUTHOR\)"!
        # TODO: Also, this currently only works case sensitive
        data_extracted = extract(data, str(book))
        if len(data_extracted) == 0:
            messagebox.showerror(
                "Nothing found",
                "Could not extract any marks or notes. There is either no "
                "book with this title or the chosen file is not a correctly "
                "formatted tolino note file. Please try again!"
            )
            opened = False  # if it was the wrong note file, open another one
            # TODO: If you just mistyped the book title you should not have
            # to open the note file again. This should get fixed as soon as
            # there is a dropdown menu to choose the books to extract (s.a.)!
            continue       
        extracted_text = format(data_extracted, str(book))
        new_path = asksaveasfilename(
            parent=root,
            title="Save notes",
            filetypes=[("Text files", "*.txt")]
        )
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
