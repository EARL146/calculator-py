
import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("340x470")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2f")

        self.expression = ""

        self.display = tk.Entry(
            root,
            font=("Arial", 24),
            justify="right",
            bg="#292940",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=10
        )
        self.display.pack(fill="x", padx=15, pady=20, ipady=12)

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]

        for row in buttons:
            frame = tk.Frame(root, bg="#1e1e2f")
            frame.pack(expand=True, fill="both", padx=10)

            for char in row:
                color = (
                    "#ff9f43" if char in ["÷", "×", "−", "+", "="]
                    else "#454560" if char not in ["C", "⌫"]
                    else "#e65c5c"
                )

                button = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 16, "bold"),
                    bg=color,
                    fg="white",
                    activebackground="#666680",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    command=lambda value=char: self.press(value)
                )
                button.pack(
                    side="left",
                    expand=True,
                    fill="both",
                    padx=4,
                    pady=4
                )

    def press(self, value):
        if value == "C":
            self.expression = ""
            self.display.delete(0, tk.END)
            return

        if value == "⌫":
            self.expression = self.expression[:-1]
            self.update_display()
            return

        if value == "=":
            self.calculate()
            return

        if value == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            elif self.expression:
                self.expression = "-" + self.expression
            else:
                self.expression = "-"
            self.update_display()
            return

        if value == "%":
            try:
                number = self.safe_evaluate()
                self.expression = str(number / 100)
                self.update_display()
            except (ValueError, ZeroDivisionError):
                self.show_error("Invalid percentage")
            return

        symbols = {
            "÷": "/",
            "×": "*",
            "−": "-"
        }

        self.expression += symbols.get(value, value)
        self.update_display()

    def safe_evaluate(self):
        import ast
        import operator

        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in operations:
                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError

                return operations[type(node.op)](left, right)

            if isinstance(node, ast.UnaryOp) and isinstance(
                node.op, (ast.UAdd, ast.USub)
            ):
                number = evaluate(node.operand)
                return number if isinstance(node.op, ast.UAdd) else -number

            raise ValueError("Invalid expression")

        tree = ast.parse(self.expression, mode="eval")
        return evaluate(tree)

    def calculate(self):
        try:
            result = self.safe_evaluate()

            if isinstance(result, float):
                result = round(result, 10)

            self.expression = str(result)
            self.update_display()

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except (ValueError, SyntaxError, OverflowError):
            self.show_error("Invalid calculation")

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def show_error(self, message):
        messagebox.showerror("Calculator Error", message)
        self.expression = ""
        self.display.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
