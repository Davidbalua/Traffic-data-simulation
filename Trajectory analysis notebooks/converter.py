import tkinter as tk
from tkinter.filedialog import askopenfile

"""
This class works as a small GUI applet, which converts .fzp data to .csv file
simply run this program
"""


class Application:
    def __init__(self):
        self.__root = tk.Tk()
        # Canvas will be a class
        self.__canvas = tk.Canvas(self.__root, width=600, height=300)
        self.__canvas.grid(columnspan=3, rowspan=3)
        self.__instruction = tk.Label(self.__root, text="insert the 'fzp' file")
        self.__instruction.grid(columnspan=3, column=0, row=1)
        self.__browse_text = tk.StringVar()
        self.__browse_button = tk.Button(self.__root, textvariable=self.__browse_text, font="Raleway", bg="#20bebe",
                                         fg="white", height=2,
                                         width=15,
                                         command=lambda: self.__on_click())
        self.__browse_text.set("Browse")
        self.__browse_button.grid(column=1, row=2)
        self.__root.mainloop()

    def __on_click(self):
        """
        this method is called, when user clicks on a button
        :return: void
        """
        self.__browse_text.set("Loading")
        # Show the open dialog box
        file = askopenfile(parent=self.__root, mode="rb", title="Choose a file", filetype=[("fzp file", "*.fzp")])
        if file:
            print("file loaded")
            # file.name shows the file directory
            with open(file.name, "r") as file:
                name = self.__split_the_name(file.name)
                print(name)

                with open(f"{name}.csv", "w") as generated_file:

                    for line in file:
                        if ("$VISION" in line) or ("*" in line):
                            pass
                        else:
                            csv_line = line.replace(";", ",")
                            generated_file.write(csv_line)
                self.__browse_text.set("File was generated")

    def __split_the_name(self, name):
        """
        this method returns the directory of the file
        :param name:
        :return: string
        """
        directory = name.split(".")[0]
        return directory


# Start the application
application = Application()
