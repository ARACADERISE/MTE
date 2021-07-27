import tkinter as tk
#from tkinter import *
import tkinter.font
import threading
import json

ALL_LEXERS = json.loads(open('languages/all_lexers.json', 'r').read())
LANGUAGE = ''

config_window = tk.Tk()
config_window.geometry("450x200")
def show(e):
    global LANGUAGE
    LANGUAGE = e.lower()
    config_window.destroy()
fr_ = tk.Frame(width = 300, height = 100)
fr_.pack()
lbl = tk.Label(fr_, text = "Language: ")
lbl.place(y = 20)
var = tk.StringVar(master = fr_)
var.set("FFL")
options = tk.OptionMenu(fr_, var, "FFL", "MFFAsm", command = show)
options.place(y = 50, width = 150)
config_window.mainloop()

INFO = json.loads(open(f'languages/{LANGUAGE}.json', 'r').read())
keywords = INFO['format']['keywords']
h = INFO['format']['highlighting']
lexer = ALL_LEXERS[LANGUAGE]
#keywords = [
#    "Settings",
#    "HasSig",
#    "true",
#    "false"
#]
#
#h = {
#    "Settings": "red",
#    "HasSig": "yellow",
#    "true": "blue",
#    "false": "blue"
#}

count = 1

NUMBER_LINE_Y_INC = 20
LAST_Y = 35
NUMBER_LINE_X = 85

curr_line = 1
curr_char = 0
l_curr_line = curr_line
l_curr_char = curr_char

w = tk.Tk()

info_frame = tk.Frame(master=w, width = 400, height = 340)
def s_line():
    c = tk.Canvas(master=w, height = 50)
    c.create_line(0, 25, 800, 25)
    c.pack()
def compile_():
    f = tk.Label(master = info_frame, text = "COMPILED!", fg = "green")
    f.after(2000, f.destroy)
    f.place(x = 160, y = 30)
w.geometry("1050x650")
#title = tk.Label(
#    text = "Moca Text Editor",
#    width = 20,
#    height = 2,
#)
#title.pack()
f = tk.Frame()
f.pack(side = tk.LEFT, fill=tk.Y, expand = False)
scrollbar = tk.Scrollbar(f)
scrollbar.pack(side = tk.RIGHT, fill=tk.Y)
text = tk.Text(f, bg="#1B1B1B", foreground="white")
text.configure(insertbackground="white")
text.pack(fill=tk.Y, expand = True)
#text.place(x = 100, y = 30, width = 400, height = 800)
#text.pack(fill=tk.X, side = tk.TOP, expand = False, pady = 0)
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)
def data():
    d = text.get(
        "1.0",
        tk.END
    )
    return d

d = ''
line_info = {1: 0}
all_lines = []
is_com = False
pad = 0
def keypress(event):
    global d
    global line_info
    global curr_char
    global l_curr_line
    global l_curr_char
    global curr_line
    global count
    global NUMBER_LINE_Y_INC
    global NUMBER_LINE_X
    global LAST_Y
    global all_lines
    global is_com
    global pad

    font = None

    d += event.char
    print(event)
    
    if event.keycode == 22:
        if curr_line > 1 and curr_char == 0:
            l_curr_line -= 1
            curr_line -= 1
            curr_char = line_info[curr_line] + 1
            if curr_line != 1:
                del line_info[curr_line]
        else:
            if curr_line > 1 and curr_char == 0:
                curr_line -= 1
                curr_char = line_info[curr_line] + 1
        if not curr_char <= 1:
            curr_char -= 1
            #l_curr_char = curr_char
        else:
            curr_char = 0
            l_curr_char = 0
            if curr_line == 1:
                line_info[1] = 0
        #print(f"CURR: {curr_line}{curr_char}, LAST: {l_curr_line}{l_curr_char}")
    elif event.keycode == 111:
        if curr_line > 1:
            if curr_char > line_info[curr_line-1]:
                #l_curr_char = curr_char
                curr_char = line_info[curr_line-1]
            
            if line_info[curr_line] == 0: curr_char = 0
            
            l_curr_char = curr_char
            l_curr_line -= 1
            curr_line -= 1
    elif event.keycode == 116:
        print(f'{curr_line}.{curr_char}')
        print(line_info)
        if curr_line + 1 in line_info:
            l_curr_char = curr_char
            curr_char = line_info[curr_line+1]
            #l_curr_line = curr_line
            curr_line += 1
    elif event.keycode == 65:
        print(f'{l_curr_line}.{l_curr_char}, {curr_line}.{curr_char}')
        #if curr_char - l_curr_char >= 7: l_curr_char += 1
        da = str(text.get(str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))).replace(' ', '')
        #for i in range(len(da)):
        #    if i == len(da) - 1: break
        #    if da[i] == '\t':
        #        l_curr_char += 4
                #curr_char += 4
        #        da = da.replace('\t', '')
        print(len(da), da)
        if da in keywords and not is_com:
            color = h[da]
            if da == 'true' or da == 'false':
                font = tkinter.font.Font(family = "serif", slant = 'italic', weight = 'bold')
            else:
                font = tkinter.font.Font(family = 'Georgia', weight = 'bold', size = 10)
        else:
            if '#' == da[0]:
                is_com = True
                color = '#CCFF00'
            elif is_com:
                color = '#CCFF00'
            else: 
                if 'x' in da:
                    color = '#00FF00'
                    font = tkinter.font.Font(family = "cursive", slant = 'italic', weight = "bold", size = 10)
                else:
                    color = "white"
                    font = tkinter.font.Font(family = "nota", weight = "normal", size = 10)
        text.tag_add(f"f{count}", str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))
        text.tag_config(f"f{count}", foreground=color, font = font)
        l_curr_char = curr_char+1
        curr_char += 1
        line_info[curr_line] += 1
        count+=1
    elif event.keycode == 36:
        da = str(text.get(str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))).replace(' ', '')
        if da in keywords and not is_com:
            color = h[da]
            if da == 'true' or da == 'false':
                font = tkinter.font.Font(family = 'serif', slant = 'italic', weight = 'bold')
            else:
                font = tkinter.font.Font(family = 'Georgia', weight = 'bold', size = 10)
        else:
            if is_com:
                is_com = False
                color = '#CCFF00'
            else:
                if 'x' in da:
                    color = '#00FF00'
                    font = tkinter.font.Font(family = "cursive", slant= 'italic', weight = "bold", size = 10)
                else:
                    color = "white"
                    font = tkinter.font.Font(family = "nota", weight = "normal", size = 10)
        #print(d)
        text.tag_add(f"f{count}", str(l_curr_line) + '.' + str(l_curr_char), str(curr_line) + '.' + str(curr_char))
        text.tag_config(f"f{count}", foreground=color, font = font)
        l_curr_char = 0
        l_curr_line = curr_line+1
        #if curr_line == 1: line_info[1] = curr_char
        #if curr_line in line_info: line_info[curr_line] += curr_char
        line_info.update({curr_line+1: 0})
        curr_line += 1
        curr_char = 0
        count+=1
        all_lines.append(curr_line)
        #n_l = tk.Label(master = f, text = f"{curr_line}")
        #n_l.place(x = NUMBER_LINE_X, y = LAST_Y)
        #LAST_Y += NUMBER_LINE_Y_INC
    else:
        if not event.keycode == 50:
            curr_char+=1
            #print(curr_line)
            line_info[curr_line] += 1

    print(f'CURR: {curr_line}.{curr_char}, LAST: {l_curr_line}.{l_curr_char}')
w.bind("<Key>", keypress)
def TAB(event = None):
    global curr_char
    global l_curr_char
    global curr_line
    global line_info

    l_curr_char = curr_char
    curr_char += 4
    line_info[curr_line] += 4

    text.insert(str(curr_line) + '.' + str(l_curr_char), '    ')
def get_lines():
    global all_lines
    
    l = tk.Label(master = info_frame, text = f"{all_lines[len(all_lines)-1] if len(all_lines) > 0 else '1'} lines")
    l.after(2000, l.destroy)
    l.place(x = 160, y = 50)

def new_window():
    n_w = tk.Tk()
    n_w.title("Settings")
    n_w.mainloop()
w.bind("<ISO_Left_Tab>", TAB)

def leave():
    w.destroy()
    
def config():
    n_w = tk.Tk()
    title = tk.Label(master = n_w, text = "Configure New Language")
    title.pack()
    n_w.geometry("400x250")
    w_f = tk.Frame(master=n_w, width = 320, height = 150)
    w_f.pack()
    
    t1 = tk.Label(master=w_f, text = "Configure Path:")
    t1.place(y = 10)
    text = tk.Text(master = w_f)
    text.place(y = 30, height = 20, width = 200)
    t2 = tk.Label(master=w_f, text = "Lexer path:")
    t2.place(y = 50)
    text2 = tk.Text(master = w_f)
    text2.place(y = 70, height = 20, width = 200)
    t3 = tk.Label(master=w_f, text = "Configure Name:")
    t3.place(y = 90)
    text3 = tk.Text(master = w_f)
    text3.place(y = 110, height = 20, width = 200)
    
    def check():
        if len(text.get('1.0', tk.END)) <= 1 or len(text2.get('1.0', tk.END)) <= 1 or len(text3.get('1.0', tk.END)) <= 1:
            err = tk.Label(master = w_f, text = "Missing fields. All fields must be filled.", fg = "red")
            err.after(1000, err.destroy)
            err.place(y=130)
        else:
            print(text.get('1.0', tk.END), '\n', text2.get('1.0', tk.END), '\n', text3.get('1.0', tk.END))
            n_w.destroy()
    
    submit = tk.Button(master = n_w, width = 15, text = "Submit", command = check)
    submit.pack()
    n_w.mainloop()
def explain():
    n_w = tk.Tk()
    ttl = tk.Label(master = n_w, text = "\n\nWelcome to MTE(Moca Text Editor)!\nAll the tools you need to write an OS with simplicity.\n\n")
    ttl.pack()
    fr = tk.Frame(master=n_w, width=1050, height=550, bg = 'white')
    fr.pack()
    n_w.geometry("1050x650")
    ab = tk.Label(master = fr, bg="white", text = 
        "\n\nMTE was created by MocaCDeveloper for users to use his file format, as well as his own assembly language, to create a sub-version of an OS\n"
        "MFF(Moca File Format), was designed to easily implement functionality for OSDev, from the bootloader, to the kernel code.\n\n"
        "MTE just gives you a place to code, where you can either create your own file format with Moca's language FFL(File Format Lang), or\n"
        "you can write MFFAsm to configure the functionality of the bootup and overall compatability of your OS.\n\n\n"
        "This MTE version is a beta version, written in Python's Tkinter module. There will be a standard release written in a more appropriate language.\n\n\n"
        "The beta versions of MTE will always be pre-released before applied to the current project. Not all beta releases will be applied to the\n"
        "standard release. So, there might be a few standard releases that come from the Python side of the project.\n\n\n"
        "Copyright, 2021. MocaCDeveloper.\nGithub: github.com/ARACADERISE\n\nAll Rights Reserved.\n\n"
    )
    ab.place(x=50, y = 50)
    
    def leave_(): n_w.destroy()
    back = tk.Button(master = fr, relief = 'flat', text = "Go Back", width = 25, command = leave_)
    back.place(x=410, y = 400)
    n_w.mainloop()

title = tk.Label(text = "\nMoca Text Editor\n\n")
title.pack()
s_line()

BUTTON_FRAME = tk.Frame(master=w)
BUTTON_FRAME.pack()
done = tk.Button(master=BUTTON_FRAME, width = 45, text = "Compile", command = compile_, relief='flat')
line = tk.Button(master=BUTTON_FRAME, width = 45, text = "Lines", command = get_lines, relief='flat')
b1 = tk.Button(master=BUTTON_FRAME, width = 45, text = "press me", command = new_window, relief = 'flat')
BUTTON_FRAME.columnconfigure(index = 0, weight = 1)
BUTTON_FRAME.columnconfigure(index = 1, weight = 1)
BUTTON_FRAME.columnconfigure(index = 2, weight = 1)
done.grid(row = 0, column = 0, padx = 50, pady = 20)
line.grid(row = 1, column = 0, padx = 50, pady = 20)
b1.grid(row = 2, column = 0, padx = 50, pady = 20)

s_line()

info_frame.pack()

menu = tk.Menu(w, bg="white")
w.config(menu=menu)
menu.add_command(label="Exit", command = leave)
menu.add_command(label="About", command = explain)
menu.add_command(label="Configure", command = config)
f_m = tk.Menu(menu)
menu.add_cascade(label='File', menu=f_m)
f_m.add_command(label='Save', command = leave)
f_m.add_command(label='Save As', command = leave)
w.mainloop()
