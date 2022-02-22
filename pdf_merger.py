from tkinter import *
from tkinter.filedialog import askopenfilenames
from PyPDF2 import PdfFileMerger
from os import startfile
import unicodedata
import re


class PDFMerger(Tk):
    def __init__(self) -> None:
        Tk.__init__(self)
        self.frame = Frame(padx=10, pady=10)
        self.frame.pack()
        self.resizable(width=False, height=False)
        self.title("PDFs merger")

        width = 400
        height = 220
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_window = screen_width // 2 - width // 2
        y_window = screen_height // 2 - height // 2
        self.geometry("%dx%d+%d+%d" % (width, height, x_window, y_window))

        self.merger = PdfFileMerger()
        self.result_name = "."

        self.choose_name_label = Label(
            self.frame,
            text="Choose the name of the merged file :",
            font=("Courrier", 13),
        )
        self.result_entry = Entry(self.frame, font=("Courrier", 13))
        self.finish_label = Label(
            self.frame, text="Choose the PDFs to merge.", font=("Courrier", 13)
        )
        self.choose_button = Button(
            self.frame,
            text="Choose files",
            command=lambda: self.merge(self.slugify(self.result_entry.get())),
            font=("Courrier", 13),
            height=1,
        )
        self.open_button = Button(
            self.frame,
            text="Open merged PDF",
            command=lambda: startfile(self.result_name),
            font=("Courrier", 13),
            state=DISABLED,
            height=1,
        )

        self.choose_name_label.pack(padx=5, pady=5)
        self.result_entry.pack(padx=5, pady=5)
        self.finish_label.pack(padx=5, pady=5)
        self.choose_button.pack(padx=5, pady=5)
        self.open_button.pack(padx=5, pady=5)

        self.mainloop()

    def merge(self, result_name: str):
        self.withdraw()
        file_names = askopenfilenames()
        ends_with_pdf = result_name.endswith(".pdf")
        for file_name in file_names:
            self.merger.append(file_name)
        if ends_with_pdf:
            self.merger.write(result_name)
            self.result_name = result_name
        else:
            self.merger.write(result_name + ".pdf")
            self.result_name = result_name + ".pdf"
        self.merger.close()
        self.open_button["state"] = NORMAL
        self.deiconify()

    def slugify(self, value, allow_unicode=False):
        """Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores."""
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize("NFKC", value)
        else:
            value = (
                unicodedata.normalize("NFKD", value)
                .encode("ascii", "ignore")
                .decode("ascii")
            )
        value = re.sub(r"[^\w\s-]", "", value.lower())
        return re.sub(r"[-\s]+", "-", value).strip("-_")


merger = PDFMerger()
