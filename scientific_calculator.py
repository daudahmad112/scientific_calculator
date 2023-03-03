import tkinter as tk
import math
import datetime

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")

        self.result = tk.Entry(master, width=20, font=('Arial', 16))
        self.result.grid(row=0, column=0, columnspan=6, pady=5)
        self.result.insert(0, "0")

        # Create buttons
        buttons = [
            "sin", "cos", "tan", "log",
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "C", "+",
            "(", ")", "=", "pi",
            "Show Log"
        ]

        # Add buttons to grid
        row = 1
        col = 0
        for button in buttons:
            command = lambda x=button: self.calculate(x)
            tk.Button(master, text=button, width=8, height=2, font=('Arial', 14), command=command, state="normal").grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Initialize counter
        self.counter = 0

    def calculate(self, key):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.counter >= 5:
            return
        if key == "=":
            try:
                result = eval(self.result.get())
                self.result.delete(0, tk.END)
                self.result.insert(0, str(result))
            except:
                self.result.delete(0, tk.END)
                self.result.insert(0, "Error")
        elif key == "C":
            self.result.delete(0, tk.END)
            self.result.insert(0, "0")
        elif key == "pi":
            self.result.insert(tk.END, math.pi)
        elif key in ["sin", "cos", "tan", "log"]:
            try:
                if key == "sin":
                    result = math.sin(float(self.result.get()))
                elif key == "cos":
                    result = math.cos(float(self.result.get()))
                elif key == "tan":
                    result = math.tan(float(self.result.get()))
                elif key == "log":
                    result = math.log(float(self.result.get()))
                self.result.delete(0, tk.END)
                self.result.insert(0, str(result))
            except:
                self.result.delete(0, tk.END)
                self.result.insert(0, "Error")
        elif key == "Show Log":
            self.show_log()
        else:
            if self.result.get() == "0":
                self.result.delete(0, tk.END)
            self.result.insert(tk.END, key)

        with open("calculations.log", "a") as f:
            f.write(f"{timestamp} - {self.result.get()}\n")

        # Increment counter and check if user is locked out
        self.counter += 1
        if self.counter >= 5:
            for button in self.master.winfo_children():
                if isinstance(button, tk.Button) and button.cget("text") != "Show Log":
                    button.config(state="disabled")

    def show_log(self):
        log_window = tk.Toplevel(self.master)
        log_window.title("Calculation Log")

        log_text = tk.Text(log_window, width=40, height=20, font=('Arial', 12))
        log_text.pack()

        with open("calculations.log", "r") as f:
            log_text.insert(tk.END, f.read())

root = tk.Tk()
my_gui = Calculator(root)
root.mainloop()
