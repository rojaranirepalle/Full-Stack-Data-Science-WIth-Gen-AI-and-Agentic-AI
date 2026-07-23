import tkinter as tkt

root = tkt.Tk()
root.title("Simple Tkinter Window")
root.geometry("300x200")

def say_hello():
    tkt.Label(root, text="Hello, Team!").pack(pady=20)

hello_button = tkt.Button(root, text="Say Hello", command=say_hello)
hello_button.pack(pady=20)

root.mainloop()
