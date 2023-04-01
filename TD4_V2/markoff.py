from tkinter import Tk, Frame

class MarkoffModelWindow(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Markoff Model", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("600x400")
        self.top_frame = Frame(self,bg='blue')
        self.bottom_frame = Frame(self,bg='pink')
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=2, uniform="group1")
        self.grid_rowconfigure(1, weight=8, uniform="group1")
        self.grid_columnconfigure(0, weight=1)

        self.state_frame = Frame(self.top_frame, bg='black')
        self.buttons_frame = Frame(self.top_frame, bg='brown')
        self.state_frame.grid(row=0, column=0, sticky="nsew")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=1, uniform="group1")
        self.top_frame.grid_rowconfigure(1, weight=1, uniform="group1")
        self.top_frame.grid_columnconfigure(0, weight=1)


new = MarkoffModelWindow()
new.mainloop()