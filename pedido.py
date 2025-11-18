"""Raíz removida: importar desde `src.models.pedido`.

Este archivo existía como wrapper de compatibilidad. Para simplificar la
estructura y evitar ambigüedades, las importaciones desde la raíz han sido
eliminadas. Importa la clase `Pedido` desde el paquete `src`:

	from src.models.pedido import Pedido

Si necesitas que mantenga compatibilidad temporal, dímelo y lo restauro.
"""

raise RuntimeError("Import desde la raíz eliminado: usa 'from src.models.pedido import Pedido'.")
