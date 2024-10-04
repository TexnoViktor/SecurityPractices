import tkinter as tk
from tkinter import filedialog, messagebox
import os

class TrithemiusCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trithemius Cipher")
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
        # Вибір типу шифрування
        self.method_label = tk.Label(self.root, text="Метод шифрування:")
        self.method_label.pack()
        self.method = tk.StringVar(value="linear")
        self.method_linear = tk.Radiobutton(self.root, text="Лінійний", variable=self.method, value="linear")
        self.method_linear.pack(anchor="w")
        self.method_nonlinear = tk.Radiobutton(self.root, text="Нелінійний", variable=self.method, value="nonlinear")
        self.method_nonlinear.pack(anchor="w")
        self.method_keyword = tk.Radiobutton(self.root, text="Гасло", variable=self.method, value="keyword")
        self.method_keyword.pack(anchor="w")

        # Введення ключів
        self.key_label = tk.Label(self.root, text="Коефіцієнти A, B (та C для нелінійного):")
        self.key_label.pack()
        self.a_entry = tk.Entry(self.root)
        self.a_entry.pack()
        self.b_entry = tk.Entry(self.root)
        self.b_entry.pack()
        self.c_entry = tk.Entry(self.root)  # Для нелінійного рівняння
        self.c_entry.pack()

        # Поле для гасла
        self.keyword_label = tk.Label(self.root, text="Гасло:")
        self.keyword_label.pack()
        self.keyword_entry = tk.Entry(self.root)
        self.keyword_entry.pack()

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

    def get_shift(self, position):
        if self.method.get() == "linear":
            A = int(self.a_entry.get())
            B = int(self.b_entry.get())
            return A * position + B
        elif self.method.get() == "nonlinear":
            A = int(self.a_entry.get())
            B = int(self.b_entry.get())
            C = int(self.c_entry.get())
            return A * (position ** 2) + B * position + C
        elif self.method.get() == "keyword":
            keyword = self.keyword_entry.get().upper()
            return ord(keyword[position % len(keyword)]) - ord('A')

    def trithemius_cipher(self, text, encrypt=True):
        alphabet_en = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = []
        for i, char in enumerate(text.upper()):
            if char in alphabet_en:
                shift = self.get_shift(i)
                if not encrypt:
                    shift = -shift
                idx = (alphabet_en.index(char) + shift) % len(alphabet_en)
                result.append(alphabet_en[idx])
            else:
                result.append(char)
        return ''.join(result)

    def encrypt_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        result = self.trithemius_cipher(text, encrypt=True)
        self.output_entry.delete("1.0", tk.END)
        self.output_entry.insert(tk.END, result)

    def decrypt_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        result = self.trithemius_cipher(text, encrypt=False)
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
        messagebox.showinfo("Про розробника", "Ця система була розроблена Виктором.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrithemiusCipherApp(root)
    root.mainloop()
