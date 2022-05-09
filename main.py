from tkinter import *

BACKGROUND_COL = "#fffff0"
FONT_TEXT = "Adobe Garamond Pro"
FONT_COL = "black"
FONT_TIME = "Helvetica"
TIME_COL = "NavajoWhite4"


class Type:
    def __init__(self):
        """ UI with text widget to type in. A bind listens for the first keypress. """
        self.window = Tk()
        self.window.title("Type or Disappear")
        self.window.config(bg=BACKGROUND_COL)

        self.length_previous_text = 0
        self.max_time = 5
        self.time_left = None
        self.timer = None

        self.current_text = StringVar()
        self.type_area = Text(
            self.window,
            width=50,
            height=30,
            bg=BACKGROUND_COL, fg=FONT_COL,
            highlightthickness=0,
            font=(FONT_TEXT, 16),
            wrap=WORD,
            spacing2=3, padx=3)
        self.type_area.grid(column=1, row=2, columnspan=2, padx=(50, 50), pady=(0, 50))
        self.current_text.set(self.type_area.get("1.0", END))
        self.type_area.bind("<KeyPress>", self.first_keypress)
        self.type_area.focus()

        self.timer_label = Label(self.window, text="", font=(FONT_TIME, 10), fg=TIME_COL, bg=BACKGROUND_COL, pady=25)
        self.timer_label.grid(column=1, row=1, columnspan=2)

        self.window.mainloop()

    def first_keypress(self, event):
        """ After the first key has appeared the bind is released and a new bind is initialised.
        The writing_activity function is initialised.
        The new bind listens for key press, the functionality cancels and hides the timer immediately.  """
        self.type_area.unbind("<KeyPress>")
        self.timer_label.config(text="")
        self.type_area.bind("<KeyPress>", self.hide_counter_asap)
        self.writing_activity(self.length_previous_text, 1, self.max_time)

    def writing_activity(self, len_old_txt, len_current_txt, time_left):
        """ Checks if there are any typing activity by comparing the length of the stringvar from 1 second earlier
         to the current stringvar. If there is no difference it means that there is no typing activity and the
         count down starts. Once time has run out, the timer is cancelled and remove_text function is initialised. """
        if len_current_txt > len_old_txt or len_current_txt < len_old_txt:
            # there is activity
            self.timer_label.config(text="")
            time_left = self.max_time
        else:
            # if len_old_txt == len_current_txt means no writing activity - start the count down
            self.timer_label.config(text=f"{time_left} seconds")
            time_left = time_left - 1
        len_old_txt = len_current_txt
        len_current_txt = len(self.current_text.get())
        self.timer = self.window.after(1000, self.writing_activity, len_old_txt, len_current_txt, time_left)
        if time_left < 0:
            self.window.after_cancel(self.timer)
            self.remove_text()

    def hide_counter_asap(self, event):
        """ Hides the count down functionality upon keypress event. Cancels and resets the timer and re-starts
        the writing_activity function. """
        self.window.after_cancel(self.timer)
        self.timer = None
        self.length_previous_text = 0
        self.writing_activity(self.length_previous_text, 1, self.max_time)

    def remove_text(self):
        """ Removes the text in the type_area. Resets the starting values including the first bind. """
        self.type_area.delete('1.0', END)
        self.length_previous_text = 0
        self.max_time = 5
        self.timer = None
        self.type_area.unbind("<KeyPress>")
        self.type_area.bind("<KeyPress>", self.first_keypress)


Type()
