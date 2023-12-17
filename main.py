import sys
import requests
import pikepdf
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from colorama import Fore, Style, init

init()  # Initialize colorama

def select_pdf_file():
    return filedialog.askopenfilename(
        title="Please select the PDF file",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )

def unlock_pdf(pdf_file, output_dir):
    unlocked = False

    try:
        pdf = pikepdf.open(pdf_file)
        output_file = output_dir / f"unlocked_{Path(pdf_file).stem}.pdf"
        pdf.save(output_file)
        pdf.close()
        unlocked = True
    except pikepdf.PasswordError:
        passwords = read_passwords()
        for pdf_password in passwords:
            try:
                pdf = pikepdf.open(pdf_file, password=pdf_password)
                output_file = output_dir / f"unlocked_{Path(pdf_file).stem}.pdf"
                pdf.save(output_file)
                pdf.close()
                unlocked = True
                break  # Exit the loop if the password is correct
            except pikepdf.PasswordError:
                continue  # Try the next password

    if unlocked:
        messagebox.showinfo("Success", "PDF unlocked successfully.")
        exit_application()  # Exit the application after handling the option

def crack_pdf(pdf_file):
    unlocked = False
    passwords = read_passwords()
    
    for pdf_password in passwords:
        try:
            pdf = pikepdf.open(pdf_file, password=pdf_password)
            pdf.close()
            unlocked = True
            decoded_password = pdf_password.decode('utf-8')  # Decode the password
            message = f"PDF unlocked successfully with the password: {decoded_password}"
            messagebox.showinfo("Success", message)
            exit_application()  # Exit the application after handling the option
            break
        except pikepdf.PasswordError:
            continue  # Try the next password

    if not unlocked:
        messagebox.showinfo("Failure", "Sorry, unable to crack the password")
        exit_application()  # Exit the application after handling the option

def read_passwords_from_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield line  # Yield the decoded line
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch passwords from the URL: {e}")

# Replace the read_passwords() function with the one below
def read_passwords():
    # Update the URL for the password file
    password_url = 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'
    return read_passwords_from_url(password_url)

def choose_operation():
    root = tk.Tk()
    root.withdraw()

    def unlock_pdf_action():
        pdf_file = select_pdf_file()
        if pdf_file:
            output_dir = Path(pdf_file).parent
            unlock_pdf(pdf_file, output_dir)

    def crack_pdf_action():
        pdf_file = select_pdf_file()
        if pdf_file:
            crack_pdf(pdf_file)

    operation_window = tk.Toplevel(root)
    operation_window.title("Welcome to PDF Unlocker Tool")

    window_width = 400
    window_height = 200

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    operation_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    button_frame = tk.Frame(operation_window)
    button_frame.pack(pady=20)  # Add some padding

    button_style = {'width': 15, 'height': 2, 'font': ('Helvetica', 12)}

    unlock_button = tk.Button(button_frame, text="Unlock PDF", command=unlock_pdf_action, **button_style)
    unlock_button.pack(pady=10)  # Add some space between buttons

    crack_button = tk.Button(button_frame, text="Crack PDF", command=crack_pdf_action, **button_style)
    crack_button.pack()

    credit_label = tk.Label(operation_window, text="Made by Taz", font=('Helvetica', 10, 'bold'), fg='green')
    credit_label.pack(pady=10)

    operation_window.protocol('WM_DELETE_WINDOW', exit_application)  # Handle the window close event

    root.mainloop()

def exit_application():
    sys.exit(0)

if __name__ == "__main__":
    choose_operation()