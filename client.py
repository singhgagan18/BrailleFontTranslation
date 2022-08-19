import socket
import threading
import tkinter
import _tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import re
import pyttsx3



HOST = '127.0.0.1'
PORT = 9090

braille = ['⠴', '⠂', '⠆', '⠒', '⠲', '⠢', '⠖', '⠶', '⠦', '⠔',
               '⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚',
               '⠅', '⠇', '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞',
               '⠥', '⠧', '⠺', '⠭', '⠽', '⠵',
               '⠱', '⠰', '⠣', '⠿', '⠀', '⠮', '⠐', '⠼', '⠫', '⠩',
               '⠯', '⠄', '⠷', '⠾', '⠡', '⠬', '⠠', '⠤', '⠨', '⠌',
               '⠜', '⠹', '⠈', '⠪', '⠳', '⠻', '⠘', '⠸']
English = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z',
               ':', ';', '<', '=', ' ', '!', '"', '#', '$', '%',
               '&', '', '(', ')', '*', '+', ',', '-', '.', '/',
               '>', '?', '@', '[', '\\', ']', '^', '_']

class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))


        msg = tkinter.Tk()
        msg.withdraw()


        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False


        self.running = True


        gui_thread = threading.Thread(target=self.gui_loop)

        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()

        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg='lightgray')


        self.chat_label = tkinter.Label(self.win, text="Chat:", bg='lightgray')
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)



        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg='lightgray')
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area= tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.button1 = tkinter.Button(self.win, text='Keyboard', command = self.mee)
        self.button1.pack(padx=20, pady=5)




        self.send_button = tkinter.Button(self.win,text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done= True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)


        self.win.mainloop()

    alphabets = [
        ['`', '⠂', '⠆', '⠒', '⠲', '⠢', '⠖', '⠶', '⠦', '⠔', '⠴', '⠤', '⠿', '⟵'],
        ['⠞⠁⠃', '⠟', '⠺', '⠑', '⠗', '⠞', '⠽', '⠥', '⠊', '⠕', '⠏', '⠪', '⠻', "⠳"],
        ['⠉⠁⠏', '⠁', '⠎', '⠙', '⠋', '⠛', '⠓', '⠚', '⠅', '⠇', '⠰', "'", '↩'],
        ['⇧', '⠵', '⠭', '⠉', '⠧', '⠃', '⠝', '⠍', '⠠', '⠨', '⠌', '⇧'],
        ['⠎⠏⠁⠉⠑']
    ]
    uppercase = False

    def mee(self):



        global uppercase
        uppercase = False

        window = tkinter.Toplevel(self.win)
        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

        for y, row in enumerate(self.alphabets):
            x = 0
            for text in row:
                if text in ('↩', '⇧'):
                    width = 15
                    columnspan = 2
                elif text == '⠎⠏⠁⠉⠑':
                    width = 130
                    columnspan = 16
                else:
                    width = 5
                    columnspan = 1



                tkinter.Button(window, text=text, width=width,
                               command=lambda value=text : self.select(self.input_area, value),
                               padx=3, pady=3, bd=12, bg="black", fg="white"
                               ).grid(row=y, column=x, columnspan=columnspan)


                x += columnspan

    def select(self,entry, value):

        global uppercase

        if value == "⠎⠏⠁⠉⠑":
            value = ' '
        elif value == '↩':
            value = '\n'
        elif value == '⠞⠁⠃':
            value = '\t'

        if value == "Backspace":
            if isinstance(entry, tkinter.Entry):
                entry.delete(len(entry.get()) - 1, 'end')
            # elif isinstance(entry, tk.Text):
            else:  # tk.Text
                entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            uppercase = not uppercase  # change True to False, or False to True
        else:
            if uppercase:
                value = value.upper()
            entry.insert('end', value)



    def write(self):
        word = self.input_area.get('1.0', 'end')
        reg = re.compile(r'[a-zA-Z]')
        if reg.match(word):
            message = f"{self.nickname}: {word}"
            print("")
            print("")
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()
            engine.stop()

        else:
            new_word = ''.join([English[braille.index(fi)] for ch in word for fi in braille if ch == fi])
            message = f"{self.nickname}: {new_word}"





        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')



    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break

            except:
                print("Error")
                self.sock.close()
                break




client = Client(HOST, PORT)














