import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

def send_message():
    message = entry.get().strip()
    if not message:
        return

    # Display your message in the chat log
    chat_log.configure(state='normal')
    chat_log.insert(tk.END, f"You: {message}\n")
    chat_log.see(tk.END)
    chat_log.configure(state='disabled')
    entry.delete(0, tk.END)

    # Send message to the server and fetch the response
    try:
        response = requests.post('http://localhost:1234/v1', json={'data': [message]})
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_data = response.json()
        
        # Check response type and handle accordingly
        if isinstance(response_data, list) and response_data:
            response_text = response_data[0]  # Access the first item if it's a list
        elif isinstance(response_data, dict) and 'message' in response_data:
            response_text = response_data['message']  # Access 'message' key if it's a dict
        else:
            response_text = "Received unrecognized format from server."
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect to server: {str(e)}")
        response_text = "Server connection failed."
    except ValueError:
        messagebox.showerror("Error", "Failed to decode JSON response.")
        response_text = "JSON decoding failed."
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        response_text = "Unexpected error occurred."

    # Display AI's response in the chat log
    chat_log.configure(state='normal')
    chat_log.insert(tk.END, f"ChatGPT: {response_text}\n")
    chat_log.see(tk.END)
    chat_log.configure(state='disabled')

# Setup the main window
root = tk.Tk()
root.title("CatGPT")
root.geometry("600x500")

chat_log = scrolledtext.ScrolledText(root, state="disabled", font=("Helvetica", 12))
chat_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=50)
entry.grid(row=0, column=0)

send_button = tk.Button(entry_frame, text="Send", font=("Helvetica", 12), command=send_message)
send_button.grid(row=0, column=1, padx=(10, 0))

root.mainloop()
