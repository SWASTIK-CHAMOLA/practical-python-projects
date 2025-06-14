
from tkinter import Tk, END, Entry, N, E, S, W, Button, font, Label
from functools import partial


def get_input(entry, argu):
    entry.insert(END, argu)


def backspace(entry):
    entry.delete(len(entry.get()) - 1)


def clear(entry):

    entry.delete(0, END)


def calc(entry):
    input_info = entry.get()
    try:

        calculator = str(eval(input_info.strip()))
    except ZeroDivisionError:

        popupmsg()
        calculator = ""
    except Exception:

        calculator = "Error"
    clear(entry)
    entry.insert(END, calculator)


def popupmsg():

    popup = Tk()
    popup.resizable(0, 0)
    popup.geometry("180x100")
    popup.title("Alert")
    label = Label(popup, text="Cannot divide by 0!\nEnter valid values")
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", bg="#DDDDDD", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def cal():

    root = Tk()
    root.title("Calculator")
    root.geometry("320x400")
    entry_font = font.Font(size=15)
    entry = Entry(root, justify="right", font=entry_font)
    entry.grid(row=0, column=0, columnspan=4, sticky=N + W + S + E, padx=5, pady=5)
    entry.focus_set()

    def key_handler(event):

        key = event.char
        keysym = event.keysym

        if keysym == 'Return':
            calc(entry)
            return "break"
        elif keysym == 'BackSpace':
            backspace(entry)
            return "break"
        elif keysym == 'Escape':
            clear(entry)
            return "break"
        elif key == '^':
            get_input(entry, '**')
            return "break"

        elif key in '0123456789.+-*/':
            # Let default behavior handle these
            return None
        else:
            # Block any other characters
            return "break"

    root.bind("<Key>", key_handler)


    cal_button_bg = '#FF6600'
    num_button_bg = '#4B4B4B'
    other_button_bg = '#DDDDDD'
    text_fg = '#FFFFFF'
    button_active_bg = '#C0C0C0'


    buttons = [
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 1, 3),
        ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 2, 3),
        ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 3, 3),
        ('0', 5, 0), ('.', 5, 1), ('^', 5, 2), ('+', 4, 3)
    ]


    for (text, r, c) in buttons:
        bg = cal_button_bg if text in '+-*/^' else num_button_bg
        # Use a lambda with a default argument to capture the correct text value
        cmd = lambda t=text: get_input(entry, '**' if t == '^' else t)
        Button(root, text=text, fg=text_fg, bg=bg, padx=10, pady=3,
               command=cmd, activebackground=button_active_bg).grid(row=r, column=c, pady=5, sticky=N + S + E + W)

    # --- Special Buttons ---
    Button(root, text='<-', bg=other_button_bg, padx=10, pady=3,
           command=lambda: backspace(entry), activebackground=button_active_bg).grid(row=1, column=0, columnspan=2,
                                                                                     padx=3, pady=5,
                                                                                     sticky=N + S + E + W)

    Button(root, text='C', bg=other_button_bg, padx=10, pady=3,
           command=lambda: clear(entry), activebackground=button_active_bg).grid(row=1, column=2, pady=5,
                                                                                 sticky=N + S + E + W)

    Button(root, text='=', fg=text_fg, bg=cal_button_bg, padx=10, pady=3,
           command=lambda: calc(entry), activebackground=button_active_bg).grid(row=5, column=3, pady=5,
                                                                                sticky=N + S + E + W)

    Button(root, text='Quit', fg='white', bg='black', command=root.quit,
           height=1, width=7).grid(row=6, column=0, columnspan=4, pady=10)

    # Configure grid weights for responsive resizing
    for i in range(1, 6):
        root.grid_rowconfigure(i, weight=1)
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)

    root.mainloop()


if __name__ == '__main__':
    cal()