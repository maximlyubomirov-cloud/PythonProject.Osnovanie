from tkinter import Tk, StringVar

root = Tk()
n1_var, d1_var, n2_var, d2_var, op_var = (StringVar(master=root) for _ in range(5))



n1_var, d1_var, n2_var, d2_var, op_var = (StringVar(master=root) for _ in range(5))

def make_digit_validator(var):
    def _check(*_):
        text = var.get()
        corrected = ''.join(c for c in text if c.isdigit())
        if text != corrected:
            var.set(corrected)
    return _check

def make_oper_validator(var):
    def _check(*_):
        text = var.get()
        corrected = ''.join(c for c in text if c in '+-*/')[:1]
        if text != corrected:
            var.set(corrected)
    return _check

n1_var.trace_add("write", make_digit_validator(n1_var))
d1_var.trace_add("write", make_digit_validator(d1_var))
n2_var.trace_add("write", make_digit_validator(n2_var))
d2_var.trace_add("write", make_digit_validator(d2_var))
op_var.trace_add("write", make_oper_validator(op_var))

# ... your Entry(...) / grid(...) / handler() code ...

root.mainloop()