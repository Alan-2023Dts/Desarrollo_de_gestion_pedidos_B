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


PRODUCTS = [
    {"id": "PIZ", "name": "Pizza Margarita", "prep_time_min": 12, "price": 8.50},
    {"id": "HMB", "name": "Hamburguesa", "prep_time_min": 8, "price": 6.00},
    {"id": "SND", "name": "Sándwich", "prep_time_min": 5, "price": 4.25},
    {"id": "ENS", "name": "Ensalada", "prep_time_min": 4, "price": 3.75},
    {"id": "BEB", "name": "Bebida 500ml", "prep_time_min": 1, "price": 1.50},
]


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
            qty = 1

        # Agregar al pedido usando la info del catálogo
        items.append({
            'name': producto['name'],
            'qty': qty,
            'prep_time_min': producto['prep_time_min'],
            'price': producto['price'],
        })

        seguir = input('¿Deseas agregar otro producto? (s/N): ').strip().lower()
        if seguir not in ('s', 'si', 'y', 'yes'):
            break

    return items


def main() -> None:

    gestor = GestorPedidos()
    gestor.estaciones['A'] = EstacionCocina('A', capacidad=2)
    gestor.estaciones['B'] = EstacionCocina('B', capacidad=3)
    gestor.estaciones['C'] = EstacionCocina('C', capacidad=1)
    gestor.estaciones['D'] = EstacionCocina('D', capacidad=3)

    print('\n=== Nuevo pedido interactivo ===')
    cliente_nombre = input('Nombre del cliente (opcional): ').strip() or None
    cliente_telefono = input('Teléfono del cliente (opcional): ').strip() or None
    cliente = {'nombre': cliente_nombre, 'telefono': cliente_telefono} if (cliente_nombre or cliente_telefono) else None

    items = elegir_productos()
    if not items:
        print('No se seleccionaron productos. Saliendo.')
        return

    pedido = gestor.crear_pedido(items, cliente_info=cliente)
    print(f'Pedido creado: id={pedido.id}')

    asignado = gestor.asignar_a_estacion(pedido.id, 'A')
    print(f'Asignado a estación A: {asignado}')

    # Calcular estimado (robusto si el temporizador falla)
    try:
        minutos = calcular_tiempo_estimado(pedido, gestor.estaciones['A'])
        if minutos is not None:
            print(f'Tiempo estimado: {minutos} minutos')
    except Exception:
        pedido.tiempo_estimado_min = getattr(pedido, 'tiempo_estimado_min', None)

    notificador = Notificador(modo='console')
    notificador.enviar(pedido, 'CREADO')
    print('Simulando preparación...')
    time.sleep(4)
    iniciados = gestor.estaciones['A'].iniciar_preparacion()
    print(f'Pedidos en preparación: {[p.id for p in iniciados]}')
    notificador.enviar(pedido, 'EN_PREPARACION')
    time.sleep(5)
    print('Simulando finalización...')
    finished = gestor.estaciones['A'].finalizar_pedido(pedido.id)
    notificador.enviar(pedido, 'FINALIZADO')
   


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrumpido por el usuario')
        sys.exit(0)
