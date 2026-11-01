from tkinter import *



def validate_entry(value):
    entry_text = value.get().strip()
    corrected_text = ''.join((b for b in entry_text if b in '0123456789'))
    if entry_text != corrected_text:
        value.delete(0, END)
        value.insert(0, corrected_text)


def validate_oper(value):
    entry_text = value.get().strip()
    corrected_text = ''.join(b for b in entry_text if b in '+-/*')
    if entry_text != corrected_text:
        value.delete(0, END)
        value.insert(0, corrected_text)


def add(n1, d1, n2, d2):
    n = n1 * d2 + n2 * d1
    d = d1 * d2
@@ -119,4 +136,9 @@ def handler():
den3.config(font=("Arial", 15), justify="center")
den3.grid(row=2, column=5)

num1.bind("<KeyRelease>", lambda event, value = num1: validate_entry(value))
den1.bind("<KeyRelease>", lambda event, value = den1: validate_entry(value))
num2.bind("<KeyRelease>", lambda event, value = num2: validate_entry(value))
den2.bind("<KeyRelease>", lambda event, value = den2: validate_entry(value))
oper.bind("<KeyRelease>", lambda event, value = oper: validate_oper(value))
root.mainloop()