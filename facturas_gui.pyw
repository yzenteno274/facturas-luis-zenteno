import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from generador_facturas import obtener_siguiente_numero, guardar_factura, generar_pdf

def calcular_totales():
    try:
        unidades = int(entry_unidades.get() or "1")
        precio = float(entry_precio.get() or "0")
        iva = float(entry_iva.get() or "21")
        base = unidades * precio
        iva_amount = base * iva / 100
        total = base + iva_amount
        label_base.config(text=f"Base: {base:,.2f} EUR")
        label_total.config(text=f"Total: {total:,.2f} EUR")
    except:
        pass

def nueva_factura():
    entry_numero.config(text=obtener_siguiente_numero())
    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_vencimiento.delete(0, tk.END)
    entry_vencimiento.insert(0, (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y"))
    entry_cliente.delete(0, tk.END)
    entry_nif.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_poblacion.delete(0, tk.END)
    entry_provincia.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_concepto.delete(0, tk.END)
    entry_unidades.delete(0, tk.END)
    entry_unidades.insert(0, "1")
    entry_precio.delete(0, tk.END)
    entry_notas.delete(0, tk.END)
    label_base.config(text="Base: 0.00 EUR")
    label_total.config(text="Total: 0.00 EUR")

def guardar():
    if not entry_cliente.get():
        messagebox.showerror("Error", "Introduce el nombre del cliente")
        return
    if not entry_concepto.get():
        messagebox.showerror("Error", "Introduce el concepto")
        return
    if not entry_precio.get():
        messagebox.showerror("Error", "Introduce el precio")
        return

    try:
        unidades = int(entry_unidades.get() or "1")
        precio = float(entry_precio.get())
        iva = float(entry_iva.get() or "21")
        base = unidades * precio
        iva_amount = base * iva / 100
        total = base + iva_amount

        datos = {
            "numero_factura": entry_numero.cget("text"),
            "fecha": entry_fecha.get(),
            "fecha_vencimiento": entry_vencimiento.get(),
            "nombre_cliente": entry_cliente.get(),
            "nif_cliente": entry_nif.get(),
            "direccion": entry_direccion.get(),
            "poblacion": entry_poblacion.get(),
            "provincia": entry_provincia.get(),
            "telefono": entry_telefono.get(),
            "email": entry_email.get(),
            "web": "",
            "concepto": entry_concepto.get(),
            "unidades": str(unidades),
            "precio_unitario": str(precio),
            "base_imponible": str(base),
            "tipo_iva": str(iva),
            "iva": str(iva_amount),
            "total": str(total),
            "notas": entry_notas.get()
        }

        guardar_factura(datos)
        archivo = generar_pdf(datos)
        messagebox.showinfo("OK", f"Factura guardada!\n\n{archivo}")
        nueva_factura()
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Generador de Facturas")
root.geometry("500x550")
root.resizable(False, False)

font_title = ("Arial", 13, "bold")
font_section = ("Arial", 11, "bold")
font_label = ("Arial", 10)
font_button = ("Arial", 11, "bold")

main_frame = tk.Frame(root, padx=12, pady=8)
main_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(main_frame, text="GENERADOR DE FACTURAS", font=font_title).grid(row=0, column=0, columnspan=6, pady=(0, 6))

tk.Label(main_frame, text="N Factura:", font=font_label).grid(row=1, column=0, sticky="w", pady=2)
entry_numero = tk.Label(main_frame, text=obtener_siguiente_numero(), font=font_label, bg="#e0e0e0", padx=5, pady=2, width=13)
entry_numero.grid(row=1, column=1, sticky="w", pady=2)

tk.Label(main_frame, text="Fecha:", font=font_label).grid(row=1, column=2, sticky="w", padx=(10, 0), pady=2)
entry_fecha = tk.Entry(main_frame, width=10)
entry_fecha.grid(row=1, column=3, sticky="w", pady=2)

tk.Label(main_frame, text="IVA %:", font=font_label).grid(row=1, column=4, sticky="w", padx=(10, 0), pady=2)
entry_iva = tk.Entry(main_frame, width=6)
entry_iva.insert(0, "21")
entry_iva.grid(row=1, column=5, sticky="w", pady=2)

tk.Label(main_frame, text="Vencimiento:", font=font_label).grid(row=2, column=0, sticky="w", pady=2)
entry_vencimiento = tk.Entry(main_frame, width=10)
entry_vencimiento.grid(row=2, column=1, sticky="w", pady=2)

tk.Frame(main_frame, height=1, bg="#cccccc").grid(row=3, column=0, columnspan=6, sticky="we", pady=6)

tk.Label(main_frame, text="DATOS DEL CLIENTE", font=font_section).grid(row=4, column=0, columnspan=6, sticky="w", pady=(0, 5))

tk.Label(main_frame, text="Nombre:", font=font_label).grid(row=5, column=0, sticky="w", pady=2)
entry_cliente = tk.Entry(main_frame, width=30)
entry_cliente.grid(row=5, column=1, columnspan=5, sticky="ew", pady=2)

tk.Label(main_frame, text="NIF:", font=font_label).grid(row=6, column=0, sticky="w", pady=2)
entry_nif = tk.Entry(main_frame, width=15)
entry_nif.grid(row=6, column=1, sticky="w", pady=2)

tk.Label(main_frame, text="Direccion:", font=font_label).grid(row=6, column=2, sticky="w", padx=(8, 0), pady=2)
entry_direccion = tk.Entry(main_frame, width=18)
entry_direccion.grid(row=6, column=3, columnspan=3, sticky="ew", pady=2)

tk.Label(main_frame, text="Poblacion:", font=font_label).grid(row=7, column=0, sticky="w", pady=2)
entry_poblacion = tk.Entry(main_frame, width=15)
entry_poblacion.grid(row=7, column=1, sticky="w", pady=2)

tk.Label(main_frame, text="Provincia:", font=font_label).grid(row=7, column=2, sticky="w", padx=(8, 0), pady=2)
entry_provincia = tk.Entry(main_frame, width=18)
entry_provincia.grid(row=7, column=3, columnspan=3, sticky="ew", pady=2)

tk.Label(main_frame, text="Telefono:", font=font_label).grid(row=8, column=0, sticky="w", pady=2)
entry_telefono = tk.Entry(main_frame, width=15)
entry_telefono.grid(row=8, column=1, sticky="w", pady=2)

tk.Label(main_frame, text="Email:", font=font_label).grid(row=8, column=2, sticky="w", padx=(8, 0), pady=2)
entry_email = tk.Entry(main_frame, width=18)
entry_email.grid(row=8, column=3, columnspan=3, sticky="ew", pady=2)

tk.Frame(main_frame, height=1, bg="#cccccc").grid(row=9, column=0, columnspan=6, sticky="we", pady=6)

tk.Label(main_frame, text="CONCEPTO", font=font_section).grid(row=10, column=0, columnspan=6, sticky="w", pady=(0, 5))

tk.Label(main_frame, text="Concepto:", font=font_label).grid(row=11, column=0, sticky="w", pady=2)
entry_concepto = tk.Entry(main_frame, width=30)
entry_concepto.grid(row=11, column=1, columnspan=5, sticky="ew", pady=2)

tk.Label(main_frame, text="Unidades:", font=font_label).grid(row=12, column=0, sticky="w", pady=2)
entry_unidades = tk.Entry(main_frame, width=8)
entry_unidades.insert(0, "1")
entry_unidades.grid(row=12, column=1, sticky="w", pady=2)

tk.Label(main_frame, text="Precio:", font=font_label).grid(row=12, column=2, sticky="w", padx=(8, 0), pady=2)
entry_precio = tk.Entry(main_frame, width=10)
entry_precio.grid(row=12, column=3, sticky="w", pady=2)
entry_precio.bind("<KeyRelease>", lambda e: calcular_totales())
entry_unidades.bind("<KeyRelease>", lambda e: calcular_totales())

tk.Label(main_frame, text="Notas:", font=font_label).grid(row=13, column=0, sticky="w", pady=2)
entry_notas = tk.Entry(main_frame, width=30)
entry_notas.grid(row=13, column=1, columnspan=5, sticky="ew", pady=2)

frame_totales = tk.Frame(main_frame, bg="#d0d0d0", padx=10, pady=8)
frame_totales.grid(row=14, column=0, columnspan=6, sticky="we", pady=12)

label_base = tk.Label(frame_totales, text="Base: 0.00 EUR", font=("Arial", 12), bg="#d0d0d0")
label_base.pack()
label_total = tk.Label(frame_totales, text="Total: 0.00 EUR", font=("Arial", 14, "bold"), bg="#d0d0d0")
label_total.pack()

btn_guardar = tk.Button(main_frame, text="GUARDAR FACTURA", font=font_button, bg="#4CAF50", fg="white", padx=15, pady=6, command=guardar)
btn_guardar.grid(row=15, column=0, columnspan=6, pady=(5, 2))

btn_nueva = tk.Button(main_frame, text="LIMPIAR", font=("Arial", 9), bg="#FF9800", fg="white", padx=8, pady=3, command=nueva_factura)
btn_nueva.grid(row=16, column=0, columnspan=6, pady=(0, 3))

nueva_factura()
root.mainloop()
