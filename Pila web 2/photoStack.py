from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Photo:
    """Representa una fotografía almacenada en el servidor."""

    photo_id: str
    filename: str
    original_name: str
    created_at: str
    size_bytes: int


class PhotoStack:
    """Administra una pila limitada de fotografías mediante LIFO."""

    def __init__(self, capacity: int = 10):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("La capacidad debe ser un entero.")

        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self._photos: list[Photo] = []
        self._capacity = capacity

    @property
    def capacity(self) -> int:
        """Devuelve la capacidad máxima."""
        return self._capacity

    @property
    def size(self) -> int:
        """Devuelve la cantidad actual de fotografías."""
        return len(self._photos)

    @property
    def is_empty(self) -> bool:
        """Indica si la pila está vacía."""
        return not self._photos

    @property
    def is_full(self) -> bool:
        """Indica si se alcanzó la capacidad máxima."""
        return self.size >= self._capacity

    @property
    def photos(self) -> list[Photo]:
        """Devuelve una copia de las fotografías."""
        return self._photos.copy()

    def push(self, photo: Photo) -> None:
        """Agrega una fotografía al tope."""
        if self.is_full:
            raise OverflowError("La pila de fotografías está llena.")

        self._photos.append(photo)

    def pop(self) -> Photo:
        """Elimina y devuelve la fotografía del tope."""
        if self.is_empty:
            raise IndexError("La pila de fotografías está vacía.")

        return self._photos.pop()

    def peek(self) -> Photo:
        """Consulta la fotografía del tope sin eliminarla."""
        if self.is_empty:
            raise IndexError("La pila de fotografías está vacía.")

        return self._photos[-1]

    def clear(self) -> list[Photo]:
        """Vacía la pila y devuelve las fotografías eliminadas."""
        removed_photos = self._photos.copy()
        self._photos.clear()

        return removed_photos

    def set_capacity(self, capacity: int) -> None:
        """Modifica la capacidad sin descartar fotografías."""
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("La capacidad debe ser un entero.")

        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        if capacity < self.size:
            raise ValueError(
                "La capacidad no puede ser inferior "
                "a la cantidad de fotografías almacenadas."
            )

        self._capacity = capacity