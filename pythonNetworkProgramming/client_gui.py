
# client_gui.py - Student's Answer Interface
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

class Client:
    def __init__(self, name, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.sendall(name.encode())
        self.gui = None
        threading.Thread(target=self.receive, daemon=True).start()

    def send_answer(self, answer):
        self.sock.sendall(f"ANSWER: {answer}".encode())

    def receive(self):
        while True:
            try:
                data = self.sock.recv(2048)
                if data:
                    self.gui.display(data.decode())
            except:
                break

class ClientGUI:
    def __init__(self, root, client):
        self.client = client
        self.client.gui = self
        self.root = root
        self.root.title("LAN Math Battle - Student")

        self.text_area = scrolledtext.ScrolledText(root, height=20, state='disabled', font=("Courier", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=10, pady=5, expand=True)
        self.entry.bind("<Return>", self.submit)

        self.send_button = tk.Button(root, text="Submit", command=self.submit, font=("Arial", 12))
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def submit(self, event=None):
        msg = self.entry.get()
        if msg.strip():
            self.client.send_answer(msg.strip())
            self.entry.delete(0, tk.END)

    def display(self, msg):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg + '\n')
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    name = simpledialog.askstring("Name", "Enter your name:", parent=root)
    client = Client(name, "localhost", 12345)  # Change IP if needed
    gui = ClientGUI(root, client)
    root.mainloop()
