# nextol - note extracting for tolino ebook reader
**nextol** extracts and formats all marks and notes of a specific ebook on the ebook reader tolino vision 4 HD. It may also work with other models of the tolino product family that use a \*.txt file with the same structure to store the notes and marks.
## Background
When you mark some text in an ebook on the tolino or take some notes on a marked text, it will store some information about this in a file named *notes.txt* (at least on the tolino vision 4 HD). You can see the data structure in the *sample_data.txt* file.

Because tolino stores the data of all ebooks in the same file, this file is very messy. Furthermore, tolino does not sort the data by books but adds new entries at the end of the file. **nextol** extracts the marks and notes from a specific ebook (but note that **nextol** removes the bookmarks as they do not give any additional information but where to read next). Then tolino removes redundant data (title, author), shortens the site number hints and removes the given metadata. Then it stores all marks and notes of the chosen ebook in a new text file.
## How to use
1. You need access to the *notes.txt* from your tolino (usually via USB) or an up-to-date copy of it.
2. You need Python 3 to execute **nextol**.
3. Start *nextol.py*, select your *notes.txt*. 
4. Type in the correct title of a book as it is listed in *notes.txt* (but without the author). It also works if you just type in a part of the title but be aware that there might be other books which titles contain this part, too, and therefore there might be some false findings. The title you type in will also be used in the header of the new file.
5. If *notes.txt* has the correct structure and you entered a valid title, choose where to store the extracted marks and notes. Otherwise, the procedure starts again with the selection of the data source.
6. At the end, the programme will ask you if you want to open the new file and if you want to extract notes from another book.

## Status and Feedback
I just created **nextol** for fun and to improve my programming skills. And of course, I wanted to have less work when extracting the marks and notes from my tolino. As this is my first public project on GitHub I would be glad about suggestions on the code. And of course, if you want to use **nextol**, too, feel free to contact me on functionality issues. Also, I would be curious to know whether this works with other ebook readers of the tolino product family. For the future (and again: just for fun), I will work with regex to extract the titles and authors from *notes.txt* in advance. That should avoid some issues with spelling mistakes or problems with the case sensitivity of the title. Also, I think of experimenting with a LaTex export instead of the new *\*.txt* file.
