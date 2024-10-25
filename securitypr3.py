import tkinter as tk
from tkinter import filedialog, messagebox
import os

class BookCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Cipher")
        self.create_menu()
        self.create_widgets()
        self.add_paste_shortcuts()  # Додаємо обробники для вставки

    def create_menu(self):
        # Створюємо меню
        menu_bar = tk.Menu(self.root)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Створити", command=self.create_file)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_command(label="Друкувати", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.exit_app)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Шифрування"
        encrypt_menu = tk.Menu(menu_bar, tearoff=0)
        encrypt_menu.add_command(label="Шифрувати", command=self.encrypt_text)
        encrypt_menu.add_command(label="Розшифрувати", command=self.decrypt_text)
        menu_bar.add_cascade(label="Шифрування", menu=encrypt_menu)

        # Меню "Допомога"
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Про розробника", command=self.show_about)
        menu_bar.add_cascade(label="Допомога", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        # Поле для вибору мови
        self.lang_label = tk.Label(self.root, text="Мова:")
        self.lang_label.pack()
        self.language = tk.StringVar(value="EN")
        self.lang_en = tk.Radiobutton(self.root, text="Англійська", variable=self.language, value="EN")
        self.lang_en.pack(anchor="w")
        self.lang_ua = tk.Radiobutton(self.root, text="Українська", variable=self.language, value="UA")
        self.lang_ua.pack(anchor="w")

        # Поле для введення вірша (ключ)
        self.poem_label = tk.Label(self.root, text="Вірш (ключ):")
        self.poem_label.pack()
        self.poem_entry = tk.Text(self.root, height=10, width=40)
        self.poem_entry.pack()

        # Поле для тексту
        self.text_label = tk.Label(self.root, text="Текст для шифрування/розшифрування:")
        self.text_label.pack()
        self.text_entry = tk.Text(self.root, height=10, width=40)
        self.text_entry.pack()

        # Поле для результату
        self.output_label = tk.Label(self.root, text="Результат:")
        self.output_label.pack()
        self.output_entry = tk.Text(self.root, height=10, width=40)
        self.output_entry.pack()

    def add_paste_shortcuts(self):
        """ Додає комбінацію Ctrl+V для полів Text """
        self.poem_entry.bind("<Control-v>", self.paste_text)
        self.text_entry.bind("<Control-v>", self.paste_text)
        self.output_entry.bind("<Control-v>", self.paste_text)

    def paste_text(self, event):
        widget = event.widget
        widget.insert(tk.INSERT, self.root.clipboard_get())
        return "break"

    def create_table(self, poem_text):
        """ Створює квадратну таблицю з тексту вірша на основі вибраної мови """
        poem_text = poem_text.upper()
        rows = poem_text.strip().splitlines()
        table = [list(row[:10]) for row in rows if row]
        return table

    def find_char_position(self, table, char):
        """ Повертає позицію символу у форматі CC/SS (рядок/стовпчик) """
        for row_idx, row in enumerate(table):
            if char in row:
                col_idx = row.index(char)
                return f"{row_idx + 1}/{col_idx + 1}"
        return None

    def book_cipher_encrypt(self, text, table):
        """ Шифрує текст за допомогою книжкового шифру """
        encrypted_text = []
        for char in text.upper():
            pos = self.find_char_position(table, char)
            if pos:
                encrypted_text.append(pos)
            else:
                encrypted_text.append(char)  # залишаємо символи, яких немає в таблиці
        return ', '.join(encrypted_text)

    def book_cipher_decrypt(self, encrypted_text, table):
        """ Розшифровує текст за допомогою книжкового шифру """
        decrypted_text = []
        for item in encrypted_text.split(', '):
            try:
                row, col = map(int, item.split('/'))
                decrypted_text.append(table[row - 1][col - 1])
            except (ValueError, IndexError):
                decrypted_text.append(item)  # залишаємо некоректні значення
        return ''.join(decrypted_text)

    def encrypt_text(self):
        poem = self.poem_entry.get("1.0", tk.END)
        text = self.text_entry.get("1.0", tk.END).strip()
        table = self.create_table(poem)
        result = self.book_cipher_encrypt(text, table)
        self.output_entry.delete("1.0", tk.END)
        self.output_entry.insert(tk.END, result)

    def decrypt_text(self):
        poem = self.poem_entry.get("1.0", tk.END)
        encrypted_text = self.text_entry.get("1.0", tk.END).strip()
        table = self.create_table(poem)
        result = self.book_cipher_decrypt(encrypted_text, table)
        self.output_entry.delete("1.0", tk.END)
        self.output_entry.insert(tk.END, result)

    def create_file(self):
        self.text_entry.delete("1.0", tk.END)
        self.output_entry.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.output_entry.get("1.0", tk.END))

    def print_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.output_entry.get("1.0", "end"))
            if os.name == 'nt':  # Windows
                os.startfile(file_path, "print")
            else:
                os.system(f"lp {file_path}")

    def exit_app(self):
        self.root.quit()

    def show_about(self):
        messagebox.showinfo("Про розробника", "Ця система була розроблена студентом групи ТВ-13 Ушаковим В.В.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookCipherApp(root)
    root.mainloop()
