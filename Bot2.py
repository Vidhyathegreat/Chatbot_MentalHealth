import tkinter as tk
from tkinter import messagebox
import json
import random
import mysql.connector
from PIL import Image, ImageTk 
import requests
from io import BytesIO

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="Vidhya@12.",  # Replace with your MySQL password
    database="chatbot_conversations"  # Ensure this matches the database you created
)

cursor = db_connection.cursor()

# Function to insert conversation into the database
def store_conversation(user_message, bot_response):
    query = "INSERT INTO conversations (user_message, bot_response) VALUES (%s, %s)"
    values = (user_message, bot_response)
    cursor.execute(query, values)
    db_connection.commit()

def chatbot_response(msg):
    # Load intents from the JSON file
    with open('intents.json') as file:
        data = json.load(file)
    
    # Convert the user message to lowercase for better matching
    msg = msg.lower()
    
    # Initialize variables to keep track of the best match
    best_match = None
    best_match_intent = None
    
    # Iterate over the intents
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # If the user's message matches a pattern, choose that intent
            if pattern.lower() in msg:
                best_match = pattern
                best_match_intent = intent
                break
    
    # If a match is found, return a random response from the corresponding intent
    if best_match_intent:
        response = random.choice(best_match_intent['responses'])
        store_conversation(msg, response)  # Store conversation in database
        return response
    
    # If no match is found, return a default response
    response = "Sorry, I didn't understand you."
    store_conversation(msg, response)  # Store conversation in database
    return response

# Function to handle login
def login():
    email = email_entry.get()
    password = password_entry.get()

    # Bypass credential check
    if email and password:
        messagebox.showinfo("Login", "Login Successful!")
        open_chatbot_window()
    else:
        messagebox.showerror("Login Error", "Please enter an email and password")

# Function to open the chatbot window
def open_chatbot_window():
    login_window.destroy()
    
    chatbot_window = tk.Tk()
    chatbot_window.title("Mental Health Chatbot")
    chatbot_window.geometry("400x500")

    chat_log = tk.Text(chatbot_window, bd=0, bg="white", height="8", width="50", font="Arial")
    chat_log.config(state=tk.DISABLED)

    scrollbar = tk.Scrollbar(chatbot_window, command=chat_log.yview, cursor="heart")
    chat_log['yscrollcommand'] = scrollbar.set

    chat_entry_box = tk.Entry(chatbot_window, bd=0, bg="white", width="29", font="Arial")
    
    send_button = tk.Button(chatbot_window, text="Send", width="12", height=5, bd=0, bg="blue", activebackground="#3c9d9b", fg='#ffffff', command=lambda: send(chat_log, chatbot_window, chat_entry_box))

    scrollbar.place(x=376, y=6, height=386)
    chat_log.place(x=6, y=6, height=386, width=370)
    chat_entry_box.place(x=6, y=400, height=90, width=265)
    send_button.place(x=275, y=400, height=90)

    chatbot_window.mainloop()

# Function to handle sending messages
def send(chat_log, chatbot_window, chat_entry_box):
    msg = chat_entry_box.get().strip()
    chat_entry_box.delete(0, tk.END)

    if msg != '':
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "You: " + msg + '\n\n')
        chat_log.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        chat_log.insert(tk.END, "Bot: " + res + '\n\n')

        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)

# Login Window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("600x400")  # Increased window size for half-screen background

# Fetch the background image from URL
background_url = "https://e1.pxfuel.com/desktop-wallpaper/950/826/desktop-wallpaper-actionable-tips-to-protect-your-chatbot-data-and-user-privacy-chatbot-thumbnail.jpg"
response = requests.get(background_url)
background_image = Image.open(BytesIO(response.content))
background_image = background_image.resize((300, 400), Image.LANCZOS)  # Resize to half the screen width

bg_img = ImageTk.PhotoImage(background_image)

# Adding background image to the left half of the login window
bg_label = tk.Label(login_window, image=bg_img)
bg_label.place(x=0, y=0, width=300, height=400)  # Cover the left half

# Create a frame for the login form on the right side
form_frame = tk.Frame(login_window)
form_frame.place(x=300, y=0, width=300, height=400)  # Cover the right half

# Add email and password fields inside the form frame
tk.Label(form_frame, text="Email").pack(pady=20)
email_entry = tk.Entry(form_frame)
email_entry.pack()

tk.Label(form_frame, text="Password").pack(pady=20)
password_entry = tk.Entry(form_frame, show="*")
password_entry.pack()

tk.Button(form_frame, text="Login", command=login).pack(pady=20)

login_window.mainloop()
