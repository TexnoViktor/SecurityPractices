import tkinter as tk
from tkinter import filedialog, messagebox
import os


class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # Створюємо меню
        menu_bar = tk.Menu(self.root)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Створити", command=self.create_file)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_command(label="Друкувати", command=self.print_file)  # Додано команду для друку
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
        # Поле для введення ключа
        self.key_label = tk.Label(self.root, text="Ключ:")
        self.key_label.pack()
        self.key_entry = tk.Entry(self.root)
        self.key_entry.pack()

        # Поле для тексту
        self.text_label = tk.Label(self.root, text="Текст для шифрування/розшифрування:")
        self.text_label.pack()
        self.text_entry = tk.Text(self.root, height=10, width=40)
        self.text_entry.pack()

        # Вибір мови
        self.lang_label = tk.Label(self.root, text="Мова:")
        self.lang_label.pack()
        self.language = tk.StringVar(value="EN")
        self.lang_en = tk.Radiobutton(self.root, text="Англійська", variable=self.language, value="EN")
        self.lang_en.pack(anchor="w")
        self.lang_ua = tk.Radiobutton(self.root, text="Українська", variable=self.language, value="UA")
        self.lang_ua.pack(anchor="w")

        # Поле для результату
        self.output_label = tk.Label(self.root, text="Результат:")
        self.output_label.pack()
        self.output_entry = tk.Text(self.root, height=10, width=40)
        self.output_entry.pack()

    def caesar_cipher(self, text, key, encrypt=True):
        alphabet_en = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphabet_ua = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
        alphabet = alphabet_en if self.language.get() == "EN" else alphabet_ua

        result = []
        shift = key if encrypt else -key

        for char in text.upper():
            if char in alphabet:
                idx = (alphabet.index(char) + shift) % len(alphabet)
                result.append(alphabet[idx])
            else:
                result.append(char)

        return ''.join(result)

    def encrypt_text(self):
        try:
            key = int(self.key_entry.get())
            text = self.text_entry.get("1.0", tk.END).strip()
            result = self.caesar_cipher(text, key, encrypt=True)
            self.output_entry.delete("1.0", tk.END)
            self.output_entry.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Invalid Key", "Key must be an integer.")

    def decrypt_text(self):
        try:
            key = int(self.key_entry.get())
            text = self.text_entry.get("1.0", tk.END).strip()
            result = self.caesar_cipher(text, key, encrypt=False)
            self.output_entry.delete("1.0", tk.END)
            self.output_entry.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Invalid Key", "Key must be an integer.")

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

    # Функція для друку файлу
    def print_file(self):
        # Спочатку зберігаємо результат шифрування/розшифрування у файл
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.output_entry.get("1.0", "end"))

            # Використовуємо системну команду для друку
            if os.name == 'nt':  # Windows
                os.startfile(file_path, "print")
            else:  # Linux / macOS
                os.system(f"lp {file_path}")

    def exit_app(self):
        self.root.quit()

    def show_about(self):
        messagebox.showinfo("Про розробника", "Ця система була розроблена студентом групи ТВ-13 Ушаковим Віктором Віталійовичем.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()
