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


def main() -> None:
    """Flujo de arranque mínimo (solo pseudocódigo y comentarios).

    Salida esperada al implementar más tarde:
    - Se crea `GestorPedidos`.
    - Se registran estaciones.
    - Se crean pedidos de ejemplo, se asignan; se calculan tiempos; se notifica eventos.
    - El script termina sin errores.
    """

    # 1) Crear gestor y recursos
    # gestor = GestorPedidos()
    # gestor.estaciones['A'] = EstacionCocina('A', capacidad=2)
    gestor = GestorPedidos()
    gestor.estaciones['A'] = EstacionCocina('A', capacidad=2)
    # 2) Crear un pedido de ejemplo
    # pedido = gestor.crear_pedido([{'name':'Pizza','qty':1,'prep_time_min':12}])
    pedido = gestor.crear_pedido([{'name':'Pizza','qty':1 ,'prep_time_min':12, 'price': 8.50}])
    # 3) Asignar a estación
    # gestor.asignar_a_estacion(pedido.id, 'A')
    gestor.asignar_a_estacion(pedido.id, 'A')
    # 4) Calcular estimado (robusto: ignorar errores del temporizador)
    try:
        calcular_tiempo_estimado(pedido, gestor.estaciones['A'])
    except Exception:
        pedido.tiempo_estimado_min = getattr(pedido, 'tiempo_estimado_min', None)
    # 5) Notificar
    # notificador = Notificador(modo='console')
    # notificador.enviar(pedido, 'CREADO')
    notificador = Notificador(modo='console')
    notificador.enviar(pedido, 'CREADO')



if __name__ == '__main__':
    main()
