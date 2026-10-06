import json
import os
import sys

# Forzar codificación UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

archivo_json = "datos_ventas.json"

# Catálogo de Componentes Electrónicos de Alta Gama
catalogo = [
    {"producto": "Procesador NeuraChip AI-X100", "precio": 850000, "stock": 3},
    {"producto": "Módulo FPGA UltraScale+ 16GB", "precio": 420000, "stock": 2},
    {"producto": "Sensor LiDAR 3D Industrial v2", "precio": 290000, "stock": 6},
    {"producto": "Microcontrolador STM32H7 Dual-Core", "precio": 85000, "stock": 12},
    {"producto": "Unidad NPU Tensor Processing V2", "precio": 650000, "stock": 1}
]

try:
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    archivo_salida = os.path.join(escritorio, "reporte_ventas.html")

    if os.path.exists(archivo_json):
        with open(archivo_json, "r", encoding="utf-8") as f:
            ventas_raw = json.load(f)

        # Enriquecer los datos del JSON con el catálogo de alta gama
        ventas = []
        for i, v in enumerate(ventas_raw):
            item = catalogo[i % len(catalogo)]
            
            p_nombre = v.get('producto') if v.get('producto') and v.get('producto') != 'Producto General' else item['producto']
            precio = v.get('precio_unitario') or v.get('precio') or item['precio']
            cantidad = v.get('cantidad', 1)
            total = precio * cantidad
            stock = max(0, item['stock'] - cantidad)
            
            ventas.append({
                'cliente': v.get('cliente') or v.get('nombre') or 'Cliente',
                'email': v.get('email', 'duoc@duoc.cl'),
                'ciudad': v.get('ciudad', 'Valparaíso'),
                'producto': p_nombre,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'total_venta': total,
                'stock_restante': stock,
                'requiere_recompra': 'SÍ (CRÍTICO)' if stock <= 2 else 'NO'
            })

        total_ingresos_dia = sum(v['total_venta'] for v in ventas)
        total_unidades = sum(v['cantidad'] for v in ventas)

        # Agrupar compras por componente
        productos = {}
        for v in ventas:
            p_nombre = v['producto']
            if p_nombre not in productos:
                productos[p_nombre] = {
                    'precio_unitario': v['precio_unitario'],
                    'unidades_vendidas': 0,
                    'recaudacion': 0,
                    'stock_restante': v['stock_restante'],
                    'requiere_recompra': v['requiere_recompra'],
                    'clientes': []
                }
            
            productos[p_nombre]['unidades_vendidas'] += v['cantidad']
            productos[p_nombre]['recaudacion'] += v['total_venta']
            productos[p_nombre]['clientes'].append({
                'nombre': v['cliente'],
                'email': v['email'],
                'ciudad': v['ciudad']
            })

        filas_productos_html = ""
        alertas_recompra_html = ""

        for prod_nombre, data in productos.items():
            lista_clientes = "<br>".join([f"• <b>{c['nombre']}</b> ({c['ciudad']}) - <i>{c['email']}</i>" for c in data['clientes']])
            
            es_critico = "SÍ" in data['requiere_recompra']
            estilo_fila = 'background-color: #fff0f0;' if es_critico else ''
            badge_stock = f"<span style='color: #dc2626; font-weight: bold;'>⚠️ {data['stock_restante']} un. (CRÍTICO)</span>" if es_critico else f"<b>{data['stock_restante']} un.</b>"

            filas_productos_html += f"""
            <tr style="{estilo_fila}">
                <td style="padding: 12px; border: 1px solid #cbd5e1; font-weight: bold; color: #0f172a;">{prod_nombre}</td>
                <td style="padding: 12px; border: 1px solid #cbd5e1;">${data['precio_unitario']:,} CLP</td>
                <td style="padding: 12px; border: 1px solid #cbd5e1; text-align: center;">{data['unidades_vendidas']}</td>
                <td style="padding: 12px; border: 1px solid #cbd5e1; text-align: right; font-weight: bold; color: #16a34a;">${data['recaudacion']:,} CLP</td>
                <td style="padding: 12px; border: 1px solid #cbd5e1; text-align: center;">{badge_stock}</td>
                <td style="padding: 12px; border: 1px solid #cbd5e1; font-size: 13px;">{lista_clientes}</td>
            </tr>
            """

            if es_critico:
                alertas_recompra_html += f"<li><b>{prod_nombre}</b>: Quedan solo <b>{data['stock_restante']} unidades</b> en laboratorio/bodega. Generar orden de compra de materia prima URGENTE.</li>"

        if not alertas_recompra_html:
            alertas_recompra_html = "<p style='color: #16a34a; margin: 0;'>✅ Inventario de componentes en niveles óptimos.</p>"
        else:
            alertas_recompra_html = f"<ul style='color: #dc2626; margin: 0; padding-left: 20px;'>{alertas_recompra_html}</ul>"

        html_contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Cierre - Fábrica de Electrónica</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background-color: #f8fafc; color: #334155;">
    <div style="max-width: 1100px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
        
        <h1 style="color: #0f172a; margin-bottom: 5px;">⚡ Reporte Diario de Ventas - Componentes de Alta Gama</h1>
        <p style="color: #64748b; font-size: 14px; margin-top: 0;">Sincronizado con MongoDB Atlas | Fábrica Semiconductora</p>

        <!-- Métricas KPI -->
        <div style="display: flex; gap: 20px; margin: 25px 0;">
            <div style="flex: 1; background: #f0fdf4; border-left: 5px solid #16a34a; padding: 18px; border-radius: 6px;">
                <span style="font-size: 12px; color: #16a34a; font-weight: bold; text-transform: uppercase;">Facturación Total del Día</span>
                <div style="font-size: 28px; font-weight: bold; color: #14532d; margin-top: 5px;">${total_ingresos_dia:,} CLP</div>
            </div>
            <div style="flex: 1; background: #eff6ff; border-left: 5px solid #2563eb; padding: 18px; border-radius: 6px;">
                <span style="font-size: 12px; color: #2563eb; font-weight: bold; text-transform: uppercase;">Componentes Despachados</span>
                <div style="font-size: 28px; font-weight: bold; color: #1e3a8a; margin-top: 5px;">{total_unidades} Unidades</div>
            </div>
        </div>

        <!-- Alerta de Stock Crítico -->
        <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 15px; border-radius: 6px; margin-bottom: 25px;">
            <h3 style="margin-top: 0; color: #991b1b; font-size: 16px;">📦 Alerta de Reabastecimiento de Componentes</h3>
            {alertas_recompra_html}
        </div>

        <!-- Tabla Detallada -->
        <h3 style="color: #1e293b;">Detalle de Ventas por Componente y Comprador</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
                <tr style="background-color: #0f172a; color: white;">
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: left;">Componente</th>
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: left;">Precio Unit.</th>
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: center;">Cant.</th>
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: right;">Total Venta</th>
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: center;">Stock Bodega</th>
                    <th style="padding: 12px; border: 1px solid #cbd5e1; text-align: left;">Cliente / Destino</th>
                </tr>
            </thead>
            <tbody>
                {filas_productos_html}
            </tbody>
        </table>

        <p style="margin-top: 30px; font-size: 11px; color: #94a3b8; text-align: center;">Sistema de Gestión de Inventario Automático n8n & Python</p>
    </div>
</body>
</html>
"""

        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(html_contenido)

        print(f"EXITO: Reporte generado correctamente en -> {archivo_salida}", flush=True)
    else:
        print(f"ERROR: No se encontro {archivo_json}", flush=True)

except Exception as e:
    print(f"ERROR: {e}", flush=True)