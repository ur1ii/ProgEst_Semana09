class Stack:
    """Implementa una pila limitada que sigue el principio LIFO."""

    def __init__(self, capacity):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("La capacidad debe ser un número entero.")

        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self._items = []
        self._capacity = capacity

    @property
    def capacity(self):
        """Devuelve la capacidad máxima de la pila."""
        return self._capacity

    @property
    def size(self):
        """Devuelve la cantidad actual de elementos."""
        return len(self._items)

    @property
    def is_empty(self):
        """Indica si la pila está vacía."""
        return len(self._items) == 0

    @property
    def is_full(self):
        """Indica si la pila alcanzó su capacidad."""
        return len(self._items) >= self._capacity

    @property
    def items(self):
        """Devuelve una copia de los elementos, del fondo al tope."""
        return self._items.copy()

    def push(self, item):
        """Agrega un elemento al tope de la pila."""
        if self.is_full:
            raise OverflowError("La pila está llena.")

        self._items.append(item)

    def pop(self):
        """Elimina y devuelve el elemento del tope."""
        if self.is_empty:
            raise IndexError("La pila está vacía.")

        return self._items.pop()

    def peek(self):
        """Consulta el elemento del tope sin eliminarlo."""
        if self.is_empty:
            raise IndexError("La pila está vacía.")

        return self._items[-1]

    def clear(self):
        """Elimina todos los elementos de la pila."""
        self._items.clear()

    def set_capacity(self, new_capacity):
        """Cambia la capacidad sin descartar elementos."""
        if not isinstance(new_capacity, int) or isinstance(
            new_capacity, bool
        ):
            raise TypeError("La capacidad debe ser un entero.")

        if new_capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        if new_capacity < self.size:
            raise ValueError(
                "La nueva capacidad no puede ser menor "
                "que la cantidad de elementos actuales."
            )

        self._capacity = new_capacity