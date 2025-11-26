import json
import os
from typing import List, Dict, Any

def leer_productos_desde_json(nombre_archivo: str) -> List[Dict[str, Any]]:
    """Lee un archivo JSON y devuelve lista de productos."""
    if not os.path.isabs(nombre_archivo):
        nombre_archivo = os.path.abspath(nombre_archivo)
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    productos: List[Dict[str, Any]] = []
    if isinstance(data, dict):
        for _, items in data.items():
            if isinstance(items, list):
                for it in items:
                    try:
                        productos.append({
                            'id': it.get('id'),
                            'name': it.get('name'),
                            'prep_time_min': int(it.get('prep_time_min', 0)),
                            'price': float(it.get('price', 0.0)),
                        })
                    except Exception:
                        continue
    elif isinstance(data, list):
        for it in data:
            try:
                productos.append({
                    'id': it.get('id'),
                    'name': it.get('name'),
                    'prep_time_min': int(it.get('prep_time_min', 0)),
                    'price': float(it.get('price', 0.0)),
                })
            except Exception:
                continue

    return productos

def guardar_productos_en_json(nombre_archivo: str, productos: List[Dict[str, Any]]) -> None:
    """Guarda la lista de productos en JSON."""
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def eliminar_producto(nombre_archivo: str, producto_id: str) -> bool:
    """Elimina un producto del archivo JSON por ID."""
    productos = leer_productos_desde_json(nombre_archivo)
    productos_filtrados = [p for p in productos if p.get('id') != producto_id]
    
    if len(productos_filtrados) < len(productos):
        guardar_productos_en_json(nombre_archivo, productos_filtrados)
        return True
    return False


def agregar_producto_json(nombre_archivo: str, producto: Dict[str, Any]) -> bool:
    """Agrega un nuevo producto al archivo JSON."""
    productos = leer_productos_desde_json(nombre_archivo)
    
    # Validar que el producto no exista
    if any(p.get('id') == producto.get('id') for p in productos):
        return False
    
    productos.append(producto)
    guardar_productos_en_json(nombre_archivo, productos)
    return True
