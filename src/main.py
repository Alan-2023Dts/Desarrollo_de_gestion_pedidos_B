"""`src.main` — punto de entrada del esqueleto dentro del paquete `src`.

Contiene la función `main()` con la secuencia de arranque y pseudocódigo
de cómo deben interactuar los componentes. No ejecuta lógica real, solo firmas
y comentarios sobre salidas esperadas.
"""
from __future__ import annotations

# Importar las clases/funciones del esqueleto (imports relativos dentro del paquete)
from .services.gestor_pedidos import GestorPedidos
from .models.estacion_cocina import EstacionCocina
from .services.notificador import Notificador
from .services.temporizador import calcular_tiempo_estimado
import sys
import time
import os
import json

PRODUCTS = [
    # Pizzas ($50-$120)
    {"id": "PIZ", "name": "Pizza Margarita", "prep_time_min": 12, "price": 50.00},
    {"id": "PIZ-PEP", "name": "Pizza de Pepperoni", "prep_time_min": 12, "price": 65.00},
    {"id": "PIZ-CHM", "name": "Pizza de Champiñones", "prep_time_min": 12, "price": 62.00},
    {"id": "PIZ-BBQ", "name": "Pizza BBQ", "prep_time_min": 13, "price": 75.00},
    {"id": "PIZ-HAM", "name": "Pizza Hawaiana", "prep_time_min": 12, "price": 70.00},
    {"id": "PIZ-4QS", "name": "Pizza 4 Quesos", "prep_time_min": 13, "price": 80.00},
    {"id": "PIZ-VEG", "name": "Pizza Vegetariana", "prep_time_min": 12, "price": 58.00},
    {"id": "PIZ-ESP", "name": "Pizza Especial", "prep_time_min": 14, "price": 120.00},
    
    # Hamburguesas ($55-$140)
    {"id": "HMB", "name": "Hamburguesa Clásica", "prep_time_min": 8, "price": 55.00},
    {"id": "HMB-DBL", "name": "Hamburguesa Doble", "prep_time_min": 10, "price": 90.00},
    {"id": "HMB-BCS", "name": "Hamburguesa con Bacon", "prep_time_min": 9, "price": 85.00},
    {"id": "HMB-CHZ", "name": "Hamburguesa con Queso", "prep_time_min": 8, "price": 65.00},
    {"id": "HMB-PIC", "name": "Hamburguesa Picante", "prep_time_min": 9, "price": 78.00},
    {"id": "HMB-EGG", "name": "Hamburguesa con Huevo", "prep_time_min": 10, "price": 95.00},
    
    # Sándwiches ($50-$110)
    {"id": "SND", "name": "Sándwich de Jamón", "prep_time_min": 5, "price": 50.00},
    {"id": "SND-POL", "name": "Sándwich de Pollo", "prep_time_min": 6, "price": 68.00},
    {"id": "SND-TUN", "name": "Sándwich de Atún", "prep_time_min": 5, "price": 75.00},
    {"id": "SND-CRN", "name": "Sándwich de Carne Asada", "prep_time_min": 7, "price": 110.00},
    {"id": "SND-VEG", "name": "Sándwich Vegetariano", "prep_time_min": 5, "price": 55.00},
    
    # Ensaladas ($60-$130)
    {"id": "ENS", "name": "Ensalada César", "prep_time_min": 4, "price": 65.00},
    {"id": "ENS-GRG", "name": "Ensalada Griega", "prep_time_min": 4, "price": 70.00},
    {"id": "ENS-POL", "name": "Ensalada de Pollo", "prep_time_min": 5, "price": 130.00},
    {"id": "ENS-MXD", "name": "Ensalada Mixta", "prep_time_min": 4, "price": 60.00},
    {"id": "ENS-CAP", "name": "Ensalada Caprese", "prep_time_min": 4, "price": 85.00},
    
    # Bebidas ($15-$35)
    {"id": "BEB", "name": "Bebida 500ml", "prep_time_min": 1, "price": 20.00},
    {"id": "BEB-JGO", "name": "Jugo Natural 300ml", "prep_time_min": 2, "price": 35.00},
    {"id": "BEB-SDA", "name": "Refresco Soda 500ml", "prep_time_min": 1, "price": 22.00},
    {"id": "BEB-CAF", "name": "Café Americano", "prep_time_min": 3, "price": 25.00},
    {"id": "BEB-LAT", "name": "Café Latte", "prep_time_min": 4, "price": 32.00},
    
    # Postres ($50-$85)
    {"id": "PST-FLN", "name": "Flan", "prep_time_min": 2, "price": 50.00},
    {"id": "PST-TPL", "name": "Tiramisu", "prep_time_min": 2, "price": 60.00},
    {"id": "PST-CHC", "name": "Cheesecake", "prep_time_min": 2, "price": 85.00},
    {"id": "PST-ARL", "name": "Arroz con Leche", "prep_time_min": 2, "price": 45.00},
    
    # Acompañamientos ($20-$50)
    {"id": "ACP-PAP", "name": "Papas Fritas", "prep_time_min": 5, "price": 35.00},
    {"id": "ACP-ONI", "name": "Aros de Cebolla", "prep_time_min": 5, "price": 40.00},
    {"id": "ACP-ALT", "name": "Alitas de Pollo", "prep_time_min": 8, "price": 75.00},
    {"id": "ACP-CHZ", "name": "Bastones de Queso", "prep_time_min": 6, "price": 50.00},
    
    # Extras/Complementos ($15-$45)
    {"id": "EXT-GSA", "name": "Guacamole", "prep_time_min": 1, "price": 28.00},
    {"id": "EXT-SAL", "name": "Salsa Picante", "prep_time_min": 1, "price": 15.00},
    {"id": "EXT-MAY", "name": "Mayonesa Extra", "prep_time_min": 1, "price": 12.00},
    {"id": "EXT-ACT", "name": "Aceitunas", "prep_time_min": 1, "price": 22.00},
]

PEDIDOS_PATH = os.path.join(os.path.dirname(__file__), '..', 'pedidos.json')


def mostrar_catalogo() -> None:
    print('\nCatálogo de productos:')
    for i, p in enumerate(PRODUCTS, start=1):
        print(f"  {i}. {p['name']} — ${p['price']:.2f} ({p['prep_time_min']} min)")


def elegir_productos() -> list[dict]:
    items: list[dict] = []
    while True:
        mostrar_catalogo()
        entrada = input('\nIntroduce el número del producto para agregar (ENTER para terminar): ').strip()
        if entrada == '':
            break
        try:
            idx = int(entrada)
            if idx < 1 or idx > len(PRODUCTS):
                print('Número fuera de rango, intenta de nuevo.')
                continue
        except ValueError:
            print('Entrada inválida, introduce un número.')
            continue

        producto = PRODUCTS[idx - 1]
        try:
            qty = int(input('Cantidad (por defecto 1): ').strip() or '1')
            if qty < 1:
                print('Cantidad mínima 1, usando 1')
                qty = 1
        except Exception:
            print('Cantidad inválida, usando 1')
            time.sleep(1)
            qty = 1

        # Agregar al pedido usando la info del catálogo
        items.append({
            'name': producto['name'],
            'qty': qty,
            'prep_time_min': producto['prep_time_min'],
            'price': producto['price'],
        })

        seguir = input('¿Deseas agregar otro producto? (s/N):\n').strip().lower()
        if seguir not in ('s', 'si', 'y', 'yes'):
            break

    return items


def guardar_pedido(pedido) -> None:
    """Guarda pedido en JSON."""
    try:
        pedidos = []
        if os.path.exists(PEDIDOS_PATH):
            with open(PEDIDOS_PATH, 'r', encoding='utf-8') as f:
                pedidos = json.load(f)

        pedidos.append(pedido.as_dict())

        with open(PEDIDOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(pedidos, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def main() -> None:

    gestor = GestorPedidos()
    gestor.estaciones['A'] = EstacionCocina('A', capacidad=2)
    gestor.estaciones['B'] = EstacionCocina('B', capacidad=3)
    gestor.estaciones['C'] = EstacionCocina('C', capacidad=1)
    gestor.estaciones['D'] = EstacionCocina('D', capacidad=3)

    os.system("cls")
    print('=== Nuevo pedido interactivo ===\n')
    cliente_nombre = input('Nombre del cliente (opcional):\n ->\t').strip() or None
    cliente_telefono = input('Teléfono del cliente (opcional):\n ->\t').strip() or None
    cliente = {'nombre': cliente_nombre, 'telefono': cliente_telefono} if (cliente_nombre or cliente_telefono) else None

    items = elegir_productos()
    if not items:
        print('No se seleccionaron productos. Saliendo.')
        return

    pedido = gestor.crear_pedido(items, cliente_info=cliente)
    print(f'Pedido creado:\n\tid:{pedido.id}')
    guardar_pedido(pedido)
    time.sleep(1)

    asignado = gestor.asignar_a_estacion(pedido.id, 'A')
    print(f'Asignado a estación A: {asignado}\n')

    # Calcular estimado (robusto si el temporizador falla)
    try:
        minutos = calcular_tiempo_estimado(pedido, gestor.estaciones['A'])
        if minutos is not None:
            print(f'Tiempo estimado: {minutos} minutos')
    except Exception:
        pedido.tiempo_estimado_min = getattr(pedido, 'tiempo_estimado_min', None)

    notificador = Notificador(modo='console')
    notificador.enviar(pedido, 'CREADO')
    time.sleep(1)
    print('\n\n\tSimulando preparación...')
    time.sleep(2)
    iniciados = gestor.estaciones['A'].iniciar_preparacion()
    print(f'Pedidos en preparación: {[p.id for p in iniciados]}')
    time.sleep(1)
    notificador.enviar(pedido, 'EN_PREPARACION')
    time.sleep(4)  
    print('\n\n\tSimulando finalización...')
    time.sleep(1)
    finished = gestor.estaciones['A'].finalizar_pedido(pedido.id)
    time.sleep(1)
    notificador.enviar(pedido, 'FINALIZADO')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrumpido por el usuario')
        sys.exit(0)
