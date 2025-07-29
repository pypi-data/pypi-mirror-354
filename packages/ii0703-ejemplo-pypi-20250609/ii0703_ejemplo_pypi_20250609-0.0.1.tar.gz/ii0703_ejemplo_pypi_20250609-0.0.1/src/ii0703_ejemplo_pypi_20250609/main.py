
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Funciones para las ventanas secundarias ---

def open_sum_window():
    # Toplevel es para crear una ventana nueva encima de la principal
    win = tk.Toplevel()
    win.title("Sumar")
    num1 = simpledialog.askinteger("Input", "Introduce el primer número:", parent=win)
    num2 = simpledialog.askinteger("Input", "Introduce el segundo número:", parent=win)
    if num1 is not None and num2 is not None:
        resultado = num1 + num2
        messagebox.showinfo("Resultado", f"La suma es: {resultado}")
    win.destroy() # Cerramos la ventana auxiliar

def open_rest_window():
    win = tk.Toplevel()
    win.title("Restar")
    num1 = simpledialog.askinteger("Input", "Introduce el primer número:", parent=win)
    num2 = simpledialog.askinteger("Input", "Introduce el segundo número:", parent=win)
    if num1 is not None and num2 is not None:
        resultado = num1 - num2
        messagebox.showinfo("Resultado", f"La resta es: {resultado}")
    win.destroy()

def show_info():
    messagebox.showinfo("Información", "Calculadora v0.0.1\nCreada para el tutorial de PyPI.")

# --- La función principal que crea la ventana ---
def main():
    root = tk.Tk()
    root.title("Calculadora ii0703")
    root.geometry("300x200")

    # Creamos un marco para organizar los botones
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Botones
    btn_sum = tk.Button(frame, text="Sumar", command=open_sum_window)
    btn_sum.pack(fill="x", pady=5)

    btn_res = tk.Button(frame, text="Restar", command=open_rest_window)
    btn_res.pack(fill="x", pady=5)

    btn_info = tk.Button(frame, text="Información", command=show_info)
    btn_info.pack(fill="x", pady=5)

    btn_exit = tk.Button(frame, text="Salir", command=root.destroy)
    btn_exit.pack(fill="x", pady=5)

    # Esto hace que la ventana se quede abierta, esperando a que hagamos algo
    root.mainloop()

# Esto es para que podamos probar el script directamente
if __name__ == "__main__":
    main()