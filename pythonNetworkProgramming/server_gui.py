# server_gui.py - Dynamic Teacher-Controlled Math Server
import socket
import threading
import tkinter as tk
from tkinter import simpledialog

clients = []
scores = {}
current_question = ""
current_answer = ""

# Send new question to all clients
def broadcast_question():
    for conn, _ in clients:
        conn.sendall(f"QUESTION: {current_question}\n".encode())

# Send updated scores to all clients
def broadcast_scores():
    scoreboard = "\nSCOREBOARD:\n" + "\n".join([f"{name}: {score}" for name, score in scores.items()])
    for conn, _ in clients:
        conn.sendall(scoreboard.encode())

def handle_client(conn, addr):
    name = conn.recv(1024).decode().strip()
    scores[name] = 0
    clients.append((conn, name))
    print(f"{name} joined from {addr}")
    if current_question:
        conn.sendall(f"QUESTION: {current_question}\n".encode())
    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if msg.startswith("ANSWER:"):
                answer = msg.split("ANSWER:")[1].strip()
                if answer == current_answer:
                    scores[name] += 10
                    conn.sendall("Correct! +10 points\n".encode())
                else:
                    conn.sendall(f"Wrong! Correct answer was {current_answer}\n".encode())
                broadcast_scores()
        except:
            break

def server_main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 12345))
    s.listen()
    print("Server listening on port 12345")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def send_new_question():
    global current_question, current_answer
    current_question = question_entry.get()
    current_answer = answer_entry.get()
    broadcast_question()

# GUI for teacher to enter questions
root = tk.Tk()
root.title("LAN Math Battle - Teacher Console")
tk.Label(root, text="Enter Question:").pack()
question_entry = tk.Entry(root, width=50)
question_entry.pack(padx=10)
tk.Label(root, text="Enter Answer:").pack()
answer_entry = tk.Entry(root, width=50)
answer_entry.pack(padx=10)
tk.Button(root, text="Send Question", command=send_new_question).pack(pady=10)

threading.Thread(target=server_main, daemon=True).start()
root.mainloop()
