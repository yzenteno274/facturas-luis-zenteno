import csv
import os
from datetime import datetime, timedelta
from fpdf import FPDF

CSV_FILE = "facturas_db.csv"
FACTURAS_DIR = "facturas"
EMPRESA = {
    "nombre": "Reformas Luis Zenteno SL",
    "direccion": "C/ Sardenya 273 ENT",
    "poblacion": "08013 Barcelona",
    "pais": "Barcelona, España",
    "nif": "B55379069"
}

def obtener_siguiente_numero():
    if not os.path.exists(CSV_FILE):
        return "2026-0001"
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        numeros = []
        for row in reader:
            num = row['numero_factura']
            if num.startswith('2026-'):
                numeros.append(int(num.split('-')[1]))
        if not numeros:
            return "2026-0001"
        return f"2026-{max(numeros) + 1:04d}"

def guardar_factura(datos):
    archivo_existe = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "numero_factura","fecha","fecha_vencimiento","nombre_cliente","nif_cliente",
            "direccion","poblacion","provincia","telefono","email","web","concepto",
            "unidades","precio_unitario","base_imponible","tipo_iva","iva","total","notas"
        ])
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(datos)

def generar_pdf(datos):
    os.makedirs(FACTURAS_DIR, exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, EMPRESA["nombre"], ln=True, align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, EMPRESA["direccion"], ln=True)
    pdf.cell(0, 5, EMPRESA["poblacion"], ln=True)
    pdf.cell(0, 5, EMPRESA["pais"], ln=True)
    pdf.cell(0, 5, f"NIF: {EMPRESA['nif']}", ln=True)

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "FACTURA", ln=True, align="R")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Numero de factura: {datos['numero_factura']}", ln=True, align="R")
    pdf.cell(0, 6, f"Fecha: {datos['fecha']}", ln=True, align="R")

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Cliente:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, datos['nombre_cliente'], ln=True)
    pdf.cell(0, 5, datos['direccion'], ln=True)
    pdf.cell(0, 5, f"{datos['poblacion']} - {datos['provincia']}", ln=True)
    pdf.cell(0, 5, f"NIF: {datos['nif_cliente']}", ln=True)
    pdf.cell(0, 5, f"Telf: {datos['telefono']}", ln=True)
    pdf.cell(0, 5, datos['email'], ln=True)

    pdf.ln(10)
    pdf.set_fill_color(200, 200, 200)
    pdf.set_font("Helvetica", "B", 9)
    headers = ["CONCEPTO", "UDS.", "BASE UD.", "BASE TOTAL", "% IVA", "IVA"]
    anchos = [60, 15, 30, 30, 20, 25]
    for i, h in enumerate(headers):
        pdf.cell(anchos[i], 8, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    base_total = float(datos['base_imponible'])
    pdf.cell(anchos[0], 7, datos['concepto'], border=1, align="L")
    pdf.cell(anchos[1], 7, datos['unidades'], border=1, align="C")
    pdf.cell(anchos[2], 7, f"{float(datos['precio_unitario']):,.2f} EUR", border=1, align="R")
    pdf.cell(anchos[3], 7, f"{base_total:,.2f} EUR", border=1, align="R")
    pdf.cell(anchos[4], 7, f"{datos['tipo_iva']}%", border=1, align="C")
    pdf.cell(anchos[5], 7, f"{float(datos['iva']):,.2f} EUR", border=1, align="R")
    pdf.ln()

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, f"Fecha de vencimiento: {datos['fecha_vencimiento']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    y_start = pdf.get_y()
    pdf.cell(120, 7, "", border=0)
    pdf.cell(35, 7, "BASE IMPONIBLE", border=1, align="C")
    pdf.cell(25, 7, f"{base_total:,.2f} EUR", border=1, align="R")
    pdf.ln()
    pdf.cell(120, 7, "", border=0)
    pdf.cell(35, 7, f"IVA ({datos['tipo_iva']}%)", border=1, align="C")
    pdf.cell(25, 7, f"{float(datos['iva']):,.2f} EUR", border=1, align="R")
    pdf.ln()
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(120, 8, "", border=0)
    pdf.cell(35, 8, "TOTAL", border=1, fill=True, align="C")
    pdf.cell(25, 8, f"{float(datos['total']):,.2f} EUR", border=1, fill=True, align="R")

    if datos.get('notas'):
        pdf.ln(15)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, f"Notas: {datos['notas']}")

    nombre_archivo = f"{FACTURAS_DIR}/{datos['numero_factura']}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo

def main():
    print("=" * 50)
    print("  GENERADOR DE FACTURAS")
    print("=" * 50)

    numero = obtener_siguiente_numero()
    print(f"\nNueva factura: {numero}")

    fecha = input("Fecha (dd/mm/aaaa) [Enter para hoy]: ").strip()
    if not fecha:
        fecha = datetime.now().strftime("%d/%m/%Y")

    fecha_venc = input("Fecha vencimiento (dd/mm/aaaa) [+30 dias]: ").strip()
    if not fecha_venc:
        fecha_venc = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")

    print("\n--- Datos del cliente ---")
    nombre = input("Nombre: ")
    nif = input("NIF: ")
    direccion = input("Direccion: ")
    poblacion = input("Poblacion: ")
    provincia = input("Provincia: ")
    telefono = input("Telefono: ")
    email = input("Email: ")
    web = input("Web: ")

    print("\n--- Detalle de factura ---")
    concepto = input("Concepto: ")
    unidades = input("Unidades [1]: ").strip() or "1"
    precio = input("Precio unitario: ")
    tipo_iva = input("Tipo IVA (21) [21]: ").strip() or "21"

    precio_f = float(precio)
    unidades_f = int(unidades)
    base = precio_f * unidades_f
    iva_f = base * float(tipo_iva) / 100
    total_f = base + iva_f

    notas = input("Notas (opcional): ")

    datos = {
        "numero_factura": numero,
        "fecha": fecha,
        "fecha_vencimiento": fecha_venc,
        "nombre_cliente": nombre,
        "nif_cliente": nif,
        "direccion": direccion,
        "poblacion": poblacion,
        "provincia": provincia,
        "telefono": telefono,
        "email": email,
        "web": web,
        "concepto": concepto,
        "unidades": unidades,
        "precio_unitario": precio,
        "base_imponible": str(base),
        "tipo_iva": tipo_iva,
        "iva": str(iva_f),
        "total": str(total_f),
        "notas": notas
    }

    print("\n--- Resumen ---")
    print(f"Base: {base:,.2f} EUR")
    print(f"IVA ({tipo_iva}%): {iva_f:,.2f} EUR")
    print(f"Total: {total_f:,.2f} EUR")

    confirmar = input("\nGuardar? (s/n): ").lower()
    if confirmar == 's':
        guardar_factura(datos)
        archivo = generar_pdf(datos)
        print(f"\n✓ Factura guardada en CSV")
        print(f"✓ PDF generado: {archivo}")
    else:
        print("Cancelado")

if __name__ == "__main__":
    main()
