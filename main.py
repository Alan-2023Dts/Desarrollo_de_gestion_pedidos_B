"""Compatibilidad: wrapper para ejecutar el entrypoint `src.main.main`.

Este archivo permite seguir ejecutando `python main.py` en la raíz durante
la transición. Recomendamos `python -m src.main`, pero este wrapper
invoca la implementación del paquete `src`.
"""
from src.main import main as _main
import sys
import time
import os
import json

ped = os.path.join(os.path.dirname(__file__), 'pedidos.json')

while True:
    op = input ("""----------MENU----------\n  1. Ingresar registro.\n  2. Ver pedidos.\n  3. Ver productos pedidos.\n
    Respuesta:\t""")
    match op:
        case '1':
            print("Iniciando gestión de pedidos...\n\n")
            time.sleep(1)
            os.system("cls")

            while True:
                comienzo = input ('¿Deseas iniciar nueva gestión de pedidos? (Si/No):\n     Respuesta:\t').strip().lower()
                match comienzo:
                    case 'si' | 's' | 'yes' | 'y':
                        print ("\nIniciando gestión de pedidos...")
                        time.sleep(1)
                        if __name__ == '__main__':
                            _main()
                    case 'no' | 'n' | 'not' | 'nop':
                        print ("\nSaliendo de la gestión de pedidos...")
                        time.sleep(.5)
                        os.system("cls")
                        break
                    case _:
                        if comienzo == '':
                            print ("\nValor blanco, intenta de nuevo.\n\n")
                            time.sleep(.5)
                            os.system("cls")
                            continue
                        elif comienzo != str:
                            print ("\nOpción inválida. Selecciona otro valor.\n\n")
                            time.sleep(.5)
                            os.system("cls")
                            continue
        case '2':
            os.system("cls")
            print('______________________________________________')
            print("----------------Ver Pedidos----------------\n")
            try:
                if os.path.exists(ped):
                    with open(ped, 'r', encoding='utf-8') as f:
                        pedidos = json.load(f)
                    
                    if pedidos:
                        print(f"Total de pedidos:\t{len(pedidos)}\n")
                        for i, p in enumerate(pedidos, 1):
                            print(f"{i}. ID: {p.get('id')} | Estado: LISTO")
                            if p.get('cliente_info'):
                                print(f"\tCliente: {p['cliente_info'].get('nombre', 'N/A')}")
                            print(f"\tTotal: ${p.get('total_price', 0):.2f}\n")
                    else:
                        print("No hay pedidos registrados.")
                else:
                    print("No hay historial de pedidos.")
            except Exception as e:
                print(f"Error: {e}")
            print('______________________________________________\n')
            input("\nPresiona ENTER para regresar al menú...")
            os.system("cls")
        
        case '3':
            os.system("cls")
            print('______________________________________________')
            print("----------------Ver Pedidos----------------\n")
            try:
                if os.path.exists(ped):
                    with open(ped, 'r', encoding='utf-8') as f:
                        pedidos = json.load(f)
                    
                    if pedidos:
                        for i, p in enumerate(pedidos, 1):
                            print(f"{i}. Pedido: {p.get('id')}")
                            for item in p.get('items', []):
                                print(f"   - {item.get('name')} x {item.get('qty')}\t(${item.get('price')*item.get('qty'):.2f})")
                            print()
                    else:
                        print("No hay pedidos registrados.")
                else:
                    print("No hay historial de pedidos.")
            except Exception as e:
                print(f"Error: {e}")
            print('______________________________________________\n')
            input("\nPresiona ENTER para regresar al menú...")
            os.system("cls")
        
        case _:
            if op == '':
                print("Valor blanco. Selecciona una opción válida.\n\n")
                time.sleep(.5)
                os.system("cls")
                continue
            elif op != str:
                print("Entrada inválida. Selecciona otro valor.\n\n")
                time.sleep(.5)
                os.system("cls")
                continue