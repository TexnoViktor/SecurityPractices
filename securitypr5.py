import tkinter as tk
from tkinter import messagebox
import random

class KnapsackCryptosystem:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.m = None
        self.t = None
        self.t_inv = None

    def generate_superincreasing_sequence(self, n):
        sequence = []
        current_sum = 0
        for _ in range(n):
            next_value = random.randint(current_sum + 1, current_sum + 10)
            sequence.append(next_value)
            current_sum += next_value
        return sequence

    def extended_gcd(self, a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = self.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    def mod_inverse(self, t, m):
        gcd, x, _ = self.extended_gcd(t, m)
        if gcd != 1:
            raise ValueError("t і m не є взаємно простими!")
        return x % m

    def generate_keys(self, n=8):
        self.private_key = self.generate_superincreasing_sequence(n)
        total_sum = sum(self.private_key)

        self.m = random.randint(total_sum + 1, total_sum + 100)
        self.t = random.randint(2, self.m - 1)
        self.t_inv = self.mod_inverse(self.t, self.m)

        self.public_key = [(self.t * bi) % self.m for bi in self.private_key]

    def encrypt(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        encrypted_blocks = []
        for block in [binary_message[i:i + len(self.public_key)] for i in range(0, len(binary_message), len(self.public_key))]:
            block_sum = sum(int(bit) * ai for bit, ai in zip(block.ljust(len(self.public_key), '0'), self.public_key))
            encrypted_blocks.append(block_sum)
        return encrypted_blocks

    def decrypt(self, encrypted_blocks):
        decrypted_message = ""
        for c in encrypted_blocks:
            s = (self.t_inv * c) % self.m
            decrypted_bits = []
            for bi in reversed(self.private_key):
                if s >= bi:
                    decrypted_bits.append(1)
                    s -= bi
                else:
                    decrypted_bits.append(0)
            decrypted_message += ''.join(map(str, reversed(decrypted_bits)))
        return ''.join(chr(int(decrypted_message[i:i + 8], 2)) for i in range(0, len(decrypted_message), 8))


class KnapsackApp:
    def __init__(self, root):
        self.crypto = KnapsackCryptosystem()
        self.root = root
        self.root.title("Криптосистема Рюкзака")

        # Поле для введення тексту
        self.text_label = tk.Label(root, text="Введіть текст для шифрування або розшифрування:")
        self.text_label.pack()
        self.text_entry = tk.Text(root, height=5, width=40)
        self.text_entry.pack()

        # Кнопка генерації ключів
        self.key_button = tk.Button(root, text="Згенерувати ключі", command=self.generate_keys)
        self.key_button.pack()

        # Поле для відображення відкритого ключа
        self.public_key_label = tk.Label(root, text="Відкритий ключ:")
        self.public_key_label.pack()
        self.public_key_text = tk.Text(root, height=2, width=40, state='disabled')
        self.public_key_text.pack()

        # Кнопки шифрування та розшифрування
        self.encrypt_button = tk.Button(root, text="Шифрувати", command=self.encrypt_message)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Розшифрувати", command=self.decrypt_message)
        self.decrypt_button.pack()

        # Поле для відображення результату
        self.result_label = tk.Label(root, text="Результат:")
        self.result_label.pack()
        self.result_text = tk.Text(root, height=5, width=40, state='disabled')
        self.result_text.pack()

    def generate_keys(self):
        self.crypto.generate_keys()
        self.public_key_text.config(state='normal')
        self.public_key_text.delete("1.0", tk.END)
        self.public_key_text.insert(tk.END, str(self.crypto.public_key))
        self.public_key_text.config(state='disabled')
        messagebox.showinfo("Успіх", "Ключі успішно згенеровані!")

    def encrypt_message(self):
        message = self.text_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Помилка", "Будь ласка, введіть текст для шифрування.")
            return
        encrypted = self.crypto.encrypt(message)
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, str(encrypted))
        self.result_text.config(state='disabled')

    def decrypt_message(self):
        encrypted = self.result_text.get("1.0", tk.END).strip()
        if not encrypted:
            messagebox.showerror("Помилка", "Будь ласка, спершу шифруйте текст перед розшифруванням.")
            return
        try:
            encrypted_blocks = list(map(int, encrypted.strip('[]').split(',')))
            decrypted = self.crypto.decrypt(encrypted_blocks)
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, decrypted)
            self.result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося розшифрувати текст: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()
