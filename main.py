import tkinter as tk
import threading

curr_line = 1
curr_char = 0
l_curr_line = curr_line
l_curr_char = curr_char

w = tk.Tk()
def compile_():
    f = tk.Label(master = w, text = "\nCOMPILED!", fg = "green")
    f.pack()
w.geometry("750x450")
title = tk.Label(
    text = "Moca Text Editor",
    width = 20,
    height = 2,
)
title.pack()
text = tk.Text(w)
text.pack(fill=tk.X)
def data():
    d = text.get(
        "1.0",
        tk.END
    )
    return d

d = ''
line_info = {}
def keypress(event):
    global d
    global line_info
    global curr_char
    global l_curr_line
    global l_curr_char
    global curr_line
    d += event.char
    print(event)
    print(f"CURR: {curr_line}.{curr_char}, LAST: {l_curr_line}.{l_curr_char}")
    if event.keycode == 22:
        if l_curr_line > 1:
            l_curr_line -= 1
            curr_line -= 1
            curr_char = line_info[curr_line]
        if not curr_char <= 1:
            curr_char -= 1
            l_curr_char = curr_char
        else:
            curr_char = 0
            l_curr_char = 0
        #print(f"CURR: {curr_line}{curr_char}, LAST: {l_curr_line}{l_curr_char}")
    elif event.keycode == 65:
        print('here')
        text.tag_add("one", str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))
        text.tag_config("one", foreground="red")
        l_curr_char = curr_char
        curr_char += 1
    elif event.keycode == 36:
        print(d)
        text.tag_add("one", str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))
        text.tag_config("one", foreground="red")
        l_curr_char = curr_char
        l_curr_line = curr_line
        line_info.update({curr_line: l_curr_char})
        curr_line += 1
        curr_char += 1
    else:
        curr_char+=1
w.bind("<Key>", keypress)
done = tk.Button(master=w, width = 12, text = "Compile", command = compile_)
done.pack()
w.mainloop()
