**Act3U-ExPrac-Bina1 — Gestión de Pedidos (Esqueleto)**

Proyecto esqueleto para gestionar pedidos en una cocina/restaurant. Este README describe la arquitectura propuesta, la lógica esperada de cada módulo, las firmas de las funciones/clases y los valores de retorno. Está pensado para servir como guía para implementar el esqueleto del proyecto y priorizar las tareas.

**Estructura del proyecto (paquetes)**

El código fuente principal está organizado en el paquete `src/`.

```
Act3U-ExPrac-Bina1/
│
└── src/                     # Código fuente organizado por paquetes
		├── __init__.py
		├── main.py              # Punto de entrada del paquete (esqueleto)
		├── models/
		│   ├── __init__.py
		│   ├── pedido.py
		│   └── estacion_cocina.py
		├── services/
		│   ├── __init__.py
		│   ├── gestor_pedidos.py
		│   ├── temporizador.py
		│   └── notificador.py
		└── utils/
				├── __init__.py
				└── utils.py
```

**Nota:**

- Este repositorio usa ahora la estructura por paquetes bajo `src/`. Se han
	eliminado los wrappers en la raíz para evitar ambigüedades y forzar la
	importación explícita desde `src.*`.


**Estructura de paquetes (detalles)**

- `src.models` : modelos de dominio como `Pedido` y `EstacionCocina`.
- `src.services` : lógica de negocio y utilidades de servicio (`GestorPedidos`, temporizador, notificador).
- `src.utils` : funciones auxiliares (generar ids, timestamps, validaciones).

**Cómo importar (recomendado)**

- Import recomendado (paquetes):

```python
from src.models.pedido import Pedido
from src.services.gestor_pedidos import GestorPedidos
from src.utils.utils import generar_id
```

- Import desde wrapper en la raíz (compatibilidad):

```python
from pedido import Pedido
from gestor_pedidos import GestorPedidos
```

La primera forma (`src.*`) es la recomendada a largo plazo.

**Cómo ejecutar**

- Ejecutar el entrypoint del paquete (recomendado cuando `src.main` esté implementado):

```powershell
python -m src.main
```

- Ejecutar el wrapper de la raíz (actualmente llama a `src.main.main()`):

```powershell
python main.py
```

Usa `python -m src.main` para evitar problemas de import relativos cuando el
proyecto crezca.

**Resumen funcional**

- **Objetivo:** Permitir crear, asignar y procesar pedidos en estaciones de cocina, estimar tiempos y notificar cambios de estado.
- **Alcance del README:** Descripción clara de clases, métodos, firmas, lógica interna y valores de retorno para guiar la implementación.

**Modelo de datos: `Pedido` (recomendado)**

- **Atributos (sugeridos):**
	- `id: str | int` : Identificador único del pedido.
	- `items: list[dict]` : Lista de ítems; cada ítem puede ser `{'name': str, 'qty': int, 'prep_time_min': int}`.
	- `estado: str` : Uno de `PENDIENTE`, `EN_PREPARACION`, `LISTO`, `ENTREGADO`, `CANCELADO`.
	- `tiempo_estimado_min: int | None` : Tiempo estimado en minutos para completar.
	- `timestamp_creado: datetime` : Fecha/hora de creación.
	- `estacion_id: str | None` : Estación asignada si aplica.
	- `cliente_info: dict | None` : Información de contacto para notificaciones (opcional).

- **Métodos esperados (alto nivel):**
	- `update_estado(nuevo_estado: str) -> None` : Validar y actualizar estado.
	- `add_item(item: dict) -> None` : Añadir ítem, recalcular estimado si aplica.
	- `remove_item(item_name: str) -> bool` : Remover ítem y devolver si se removió.

**Detalles por módulo**

**`pedido.py`**
- **Clase:** `Pedido`
- **Responsabilidad:** Representar un pedido y encapsular operaciones simples sobre él.
- **Interfaces (firmas sugeridas):**
	- `class Pedido:`
		- `def __init__(self, id: str|int, items: list[dict], cliente_info: dict | None = None) -> None`
			- Crea un pedido; setea `estado='PENDIENTE'`, `timestamp_creado` y `tiempo_estimado_min=None`.
		- `def update_estado(self, nuevo_estado: str) -> None`
			- Valida transiciones de estado (por ejemplo PENDIENTE -> EN_PREPARACION -> LISTO -> ENTREGADO).
			- Lanza `ValueError` si la transición no es válida.
		- `def add_item(self, item: dict) -> None`
			- Añade item; recalcula `tiempo_estimado_min` opcionalmente.
		- `def remove_item(self, item_name: str) -> bool`
			- Elimina item por nombre; devuelve `True` si se eliminó, `False` si no existe.
		- `def as_dict(self) -> dict`
			- Devuelve representación serializable.

**Retornos y excepciones:**
- Métodos que mutan normalmente retornan `None` y levantan `ValueError` en errores de validación.

**`estacion_cocina.py`**
- **Clase:** `EstacionCocina`
- **Responsabilidad:** Modelar una estación de trabajo que puede aceptar y procesar pedidos (cola local).
- **Interfaces (firmas sugeridas):**
	- `class EstacionCocina:`
		- `def __init__(self, id: str, capacidad: int = 1) -> None`
			- `capacidad`: número de pedidos que puede preparar en paralelo.
		- `def asignar_pedido(self, pedido: Pedido) -> bool`
			- Añade el pedido a la cola si hay capacidad; devuelve `True` si se asignó.
		- `def iniciar_preparacion(self) -> list[Pedido]`
			- Marca los pedidos que empiezan a prepararse; devuelve lista de pedidos en preparación.
		- `def finalizar_pedido(self, pedido_id: str|int) -> bool`
			- Marca un pedido como `LISTO`; devuelve `True` si tuvo éxito.
		- `def carga_actual(self) -> int`
			- Devuelve número de pedidos en cola/ocupando la estación.

**Comportamiento y concurrencia:**
- Inicialmente la estación puede implementarse sin concurrencia (síncrona). Para ejecución real se recomienda usar hilos (`threading`) o `asyncio` para simular trabajos en paralelo.

**`gestor_pedidos.py`**
- **Clase:** `GestorPedidos`
- **Responsabilidad:** Orquestar creación, almacenamiento y asignación de pedidos a estaciones.
- **Interfaces (firmas sugeridas):**
	- `class GestorPedidos:`
		- `def __init__(self) -> None`
			- Mantiene estructuras en memoria: `pedidos: dict[id, Pedido]`, `estaciones: dict[id, EstacionCocina]`.
		- `def crear_pedido(self, items: list[dict], cliente_info: dict | None = None) -> Pedido`
			- Crea y registra un `Pedido`, devuelve la instancia.
		- `def cancelar_pedido(self, pedido_id: str|int) -> bool`
			- Cancela si está permitido; devuelve `True` si se canceló.
		- `def asignar_a_estacion(self, pedido_id: str|int, estacion_id: str) -> bool`
			- Intenta asignar el pedido a la estación; devuelve `True` si se logró.
		- `def obtener_pedido(self, pedido_id: str|int) -> Pedido | None`
		- `def listar_pedidos(self, estado: str | None = None) -> list[Pedido]`

**Retornos y errores:**
- `crear_pedido` devuelve la instancia `Pedido` creada. Métodos de mutación devuelven `bool` indicando éxito/fracaso.

**`temporizador.py`**
- **Responsabilidad:** Calcular estimaciones de tiempo para pedidos.
- **API recomendada:**
	- `def calcular_tiempo_estimado(pedido: Pedido, estacion: EstacionCocina | None = None) -> int`
		- Devuelve tiempo estimado en minutos (int). Lógica: sumar `prep_time_min` de cada ítem, ajustar por carga de estación (p.ej. añadir penalización por cola).
	- `def formato_tiempo(minutos: int) -> str`
		- Devuelve texto legible, p.ej. `"25 min"` o `"1h 5min"`.

**Comportamiento esperado:**
- Si los ítems no tienen `prep_time_min`, usar heurística por tipo o valor por defecto (ej. 5 minutos por ítem).

**`notificador.py`**
- **Responsabilidad:** Simular envío de notificaciones al cliente (prints, logs o integración con websockets/webhooks).
- **API recomendada:**
	- `class Notificador:`
		- `def __init__(self, modo: str = 'console') -> None`  # modos: 'console', 'email', 'webhook'
		- `def enviar(self, pedido: Pedido, evento: str, extra: dict | None = None) -> bool`
			- Envía notificación; devuelve `True` si la entrega simulada tuvo éxito.

**`main.py`**
- **Responsabilidad:** Armar y arrancar las piezas: crear `GestorPedidos`, instanciar estaciones, y simular flujo de pedidos.
- **Ejemplo de flujo mínimo (pseudocódigo):**

```python
from gestor_pedidos import GestorPedidos
from estacion_cocina import EstacionCocina
from notificador import Notificador

gestor = GestorPedidos()
gestor.estaciones['A'] = EstacionCocina('A', capacidad=2)
notificador = Notificador()

pedido = gestor.crear_pedido([{'name':'Pizza','qty':1,'prep_time_min':12}])
gestor.asignar_a_estacion(pedido.id, 'A')
# temporizador.calcular_tiempo_estimado(pedido)
notificador.enviar(pedido, 'CREADO')
```

**Flujo de ejecución detallado**

1. `main.py` crea `GestorPedidos` y registra `EstacionCocina`(s).
2. Cliente o flujo de pruebas llama `gestor.crear_pedido(...)` -> se crea `Pedido` con `estado='PENDIENTE'`.
3. `gestor.asignar_a_estacion(...)` intenta insertar el pedido en la estación; si es posible, `pedido.estacion_id` se actualiza y `pedido.update_estado('EN_PREPARACION')` es invocado.
4. `temporizador.calcular_tiempo_estimado(pedido, estacion)` calcula y escribe `pedido.tiempo_estimado_min`.
5. Cuando la preparación termina (simulada por `EstacionCocina.finalizar_pedido` o por un temporizador/hilo), se llama `pedido.update_estado('LISTO')` y `Notificador.enviar(pedido, 'LISTO')`.
6. Finalmente, al entregar, `pedido.update_estado('ENTREGADO')` y notificar.

**Consideraciones de implementación**

- **Persistencia:** Para el esqueleto, usar estructura en memoria (`dict`). Para producción, usar base de datos (SQLite, Postgres).
- **Concurrencia:** Si desea simulación paralela de preparación, use `threading.Thread` por estación o `asyncio` con `async/await`.
- **Validación de estados:** Centralizar la lógica de transiciones en `Pedido.update_estado` para evitar inconsistencias.
- **Pruebas unitarias:** Añadir pruebas para transiciones de estado, calculadora de tiempos y asignación a estaciones.
- **Logging:** Registrar eventos críticos (creación, asignación, errores) con `logging` en vez de `prints`.

**Errores y excepciones recomendadas**

- `ValueError` para entradas inválidas (ej. estado desconocido, items mal formados).
- `KeyError` o `LookupError` cuando un `pedido_id` no exista (o devolver `None` según preferencia API).

**Checklist de implementación (prioridad sugerida)**

- **Alta:**
	- Implementar `Pedido` mínimo en `pedido.py` (atributos, `update_estado`, `as_dict`).
	- Implementar `GestorPedidos.crear_pedido`, `obtener_pedido` y almacenamiento en memoria.
	- Implementar `EstacionCocina` con cola básica y `asignar_pedido`.
- **Media:**
	- Implementar `temporizador.calcular_tiempo_estimado` y hooking en creación/asignación.
	- Implementar `Notificador` con modo `console`.
- **Baja / Opcional:**
	- Soporte de concurrencia (hilos/asyncio) para preparación en background.
	- Persistencia en fichero/DB.
	- Integración con tests automatizados.

**Ejecutar (esqueleto/PRUEBA rápida)**

1. Asegurarse de tener Python 3.8+.
2. Ejecutar el `main.py` simple (cuando esté creado):

```powershell
python main.py
```

**Ejemplo de README: tareas a implementar ahora**

- Implementar `pedido.py` con la clase `Pedido` y pruebas unitarias básicas.
- Implementar `gestor_pedidos.py` con almacenamiento en memoria.
- Crear una `main.py` mínima que cree un pedido y lo asigne a una estación.
 
**Lista de implementación (paso a paso)**

Esta lista guía la implementación desde el inicio hasta tener un esqueleto funcional. Cada paso incluye objetivo, estimación rápida y criterios de aceptación mínimos.

1) Preparar entorno y repo
	- Objetivo: Tener Python 3.8+ disponible y el repo listo.
	- Estimación: 5–10 min
	- Acciones:
		- Crear/activar entorno virtual: `python -m venv .venv` ; `.\.venv\Scripts\Activate.ps1` (PowerShell)
		- Añadir `requirements.txt` si se usan dependencias.
	- Criterio de aceptación: `python -V` muestra versión >=3.8 y entorno activado.

2) Implementar `pedido.py` (modelo básico)
	- Objetivo: Clase `Pedido` con atributos y métodos básicos (`update_estado`, `as_dict`, `add_item`, `remove_item`).
	- Estimación: 30–60 min
	- Criterio de aceptación: Crear instancia `Pedido` en REPL, cambiar estado válido y obtener `as_dict()` sin errores.
	- Nota: Centralizar validaciones de transición de estado.

3) Implementar `gestor_pedidos.py` (almacenamiento en memoria)
	- Objetivo: Registrar pedidos, obtener, listar y cancelar.
	- Estimación: 30–60 min
	- Criterio de aceptación: `GestorPedidos.crear_pedido(...)` devuelve `Pedido`, `obtener_pedido(id)` lo recupera.

4) Implementar `estacion_cocina.py` (cola básica)
	- Objetivo: Clase `EstacionCocina` con cola simple y `asignar_pedido`/`finalizar_pedido`.
	- Estimación: 45–90 min
	- Criterio de aceptación: Asignar pedido a estación y comprobar `carga_actual()` incrementada; `finalizar_pedido` marca `LISTO`.

5) Integración mínima en `main.py`
	- Objetivo: Script que crea gestor, instancia una estación, crea un pedido y lo asigna (flujo mínimo).
	- Estimación: 15–30 min
	- Criterio de aceptación: Ejecutar `python main.py` y ver la simulación (prints/logs) sin excepciones.

6) Implementar `temporizador.py` (estimación de tiempo)
	- Objetivo: Función `calcular_tiempo_estimado` que sume `prep_time_min` y ajuste por carga.
	- Estimación: 30–60 min
	- Criterio de aceptación: Llamar la función con un pedido y obtener un entero >0; `pedido.tiempo_estimado_min` se actualiza.

7) Implementar `notificador.py` (modo consola)
	- Objetivo: Notificador que emita messages por consola/logging cuando cambien estados relevantes.
	- Estimación: 20–40 min
	- Criterio de aceptación: Al cambiar un pedido a `LISTO`, se imprime/ registra notificación.

8) Pruebas unitarias básicas
	- Objetivo: Añadir tests para `Pedido` (transiciones), `temporizador` y `GestorPedidos`.
	- Estimación: 60–120 min
	- Herramienta: `pytest` (opcional)
	- Criterio de aceptación: Tests clave pasan localmente.

9) Mejora: Simular preparación (concurrencia básica)
	- Objetivo: Simular que la estación procesa pedidos en background (hilos o asyncio).
	- Estimación: 1–3 horas (dependiendo de la opción)
	- Criterio de aceptación: Múltiples pedidos pueden estar `EN_PREPARACION` y finalizar tras temporizador simulado.

10) Persistencia ligera (opcional)
	- Objetivo: Guardar/recuperar estado en disco (JSON o SQLite) al reiniciar la app.
	- Estimación: 1–2 horas
	- Criterio de aceptación: Reiniciar `main.py` preserva pedidos no entregados.

11) Logging y manejo de errores
	- Objetivo: Reemplazar `print` por `logging`, añadir manejo claro de excepciones en las API públicas.
	- Estimación: 30–90 min
	- Criterio de aceptación: Eventos importantes registrados en consola/archivo con niveles adecuados.

12) Documentación y entrega
	- Objetivo: Finalizar README (esta sección incluida), ejemplos de uso y checklist para revisión.
	- Estimación: 30–60 min
	- Criterio de aceptación: README actualizado con pasos para ejecutar y explicar las APIs principales.

Comandos útiles (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt  # si aplica
pytest -q  # ejecutar tests
python main.py
```

Sugerencia de prioridades: seguir pasos 1→5 para tener un esqueleto funcional en pocas horas, luego 6→8 para mejorar comportamiento y testeo, y por último 9→11 para robustez y producción.
 

---
_Este README es una guía de diseño. Ajusta las firmas y las decisiones (p. ej. excepciones vs valores de retorno) al estilo de código del equipo._
