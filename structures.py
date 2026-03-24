"""
ESTRUCTURAS DE DATOS - Sistema de Triage Hospitalario
Implementa: Array, Pila, Cola, Lista Enlazada Simple y Lista (Python nativa)
"""

from datetime import datetime
import time


# ─────────────────────────────────────────────
# 1. ARRAY (arreglo de tamaño fijo)
# ─────────────────────────────────────────────
class Array:
    """Array de tamaño fijo para almacenar camas disponibles por sala."""

    def __init__(self, size: int):
        self.size = size
        self.data = [None] * size  # slots inicializados en None

    def set(self, index: int, value):
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError(f"Índice {index} fuera de rango (0-{self.size - 1})")

    def get(self, index: int):
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError(f"Índice {index} fuera de rango")

    def available_slots(self):
        return [i for i, v in enumerate(self.data) if v is None]

    def occupied_slots(self):
        return [(i, v) for i, v in enumerate(self.data) if v is not None]

    def is_full(self):
        return all(v is not None for v in self.data)

    def __repr__(self):
        return f"Array({self.data})"


# ─────────────────────────────────────────────
# 2. PILA (Stack - LIFO)
# ─────────────────────────────────────────────
class Stack:
    """Pila LIFO para historial de acciones (undo/redo de atenciones)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(reversed(self._items))

    def __repr__(self):
        return f"Stack(top→{self._items[-1] if self._items else 'vacía'})"


# ─────────────────────────────────────────────
# 3. COLA (Queue - FIFO) con prioridad
# ─────────────────────────────────────────────
class PriorityQueue:
    """
    Cola de prioridad FIFO para pacientes en espera.
    Prioridad: 1=Rojo(crítico) > 2=Naranja > 3=Amarillo > 4=Verde > 5=Azul
    """

    def __init__(self):
        self._queue = []

    def enqueue(self, patient):
        """Inserta en orden de prioridad; igual prioridad → FIFO por timestamp."""
        self._queue.append(patient)
        # Ordenar: prioridad ASC, luego tiempo ASC
        self._queue.sort(key=lambda p: (p["priority"], p["timestamp"]))

    def dequeue(self):
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self._queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self._queue[0]

    def remove_by_id(self, patient_id: str):
        self._queue = [p for p in self._queue if p["id"] != patient_id]

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def to_list(self):
        return list(self._queue)

    def __repr__(self):
        return f"PriorityQueue(size={len(self._queue)})"


# ─────────────────────────────────────────────
# 4. LISTA ENLAZADA SIMPLE (Singly Linked List)
# ─────────────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """
    Lista enlazada simple para el registro cronológico de eventos del sistema
    (audit log). Inserta al frente para O(1).
    """

    def __init__(self):
        self.head = None
        self._size = 0

    def prepend(self, data):
        """Inserta al inicio — O(1)."""
        node = Node(data)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, data):
        """Inserta al final — O(n)."""
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self._size += 1

    def delete(self, data):
        """Elimina primer nodo con data igual."""
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        cur = self.head
        while cur.next:
            if cur.next.data == data:
                cur.next = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False

    def search(self, key, field=None):
        """Busca un nodo. Si field es dado, busca dentro de dict."""
        cur = self.head
        while cur:
            if field:
                if isinstance(cur.data, dict) and cur.data.get(field) == key:
                    return cur.data
            else:
                if cur.data == key:
                    return cur.data
            cur = cur.next
        return None

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def size(self):
        return self._size

    def __repr__(self):
        return f"SinglyLinkedList(size={self._size})"


# ─────────────────────────────────────────────
# 5. LISTA (Python list) — pacientes dados de alta
# ─────────────────────────────────────────────
class DischargeList:
    """
    Lista nativa Python para pacientes dados de alta.
    Permite búsqueda, filtros y estadísticas rápidas.
    """

    def __init__(self):
        self._data: list = []

    def add(self, patient: dict):
        self._data.append(patient)

    def remove(self, patient_id: str):
        self._data = [p for p in self._data if p["id"] != patient_id]

    def get_by_id(self, patient_id: str):
        return next((p for p in self._data if p["id"] == patient_id), None)

    def filter_by_priority(self, priority: int):
        return [p for p in self._data if p["priority"] == priority]

    def sort_by_discharge_time(self):
        return sorted(self._data, key=lambda p: p.get("discharge_time", 0))

    def count(self):
        return len(self._data)

    def all(self):
        return list(self._data)

    def __repr__(self):
        return f"DischargeList(count={len(self._data)})"
