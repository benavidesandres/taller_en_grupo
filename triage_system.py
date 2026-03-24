"""
BACKEND — Sistema de Triage y Flujo de Sala de Urgencias
Orquesta todas las estructuras de datos definidas en structures.py
"""

import uuid
import time
from datetime import datetime
from structures import Array, Stack, PriorityQueue, SinglyLinkedList, DischargeList

# ─────────────────────────────────────────────
# Constantes de Triage (escala Manchester)
# ─────────────────────────────────────────────
TRIAGE_LEVELS = {
    1: {"name": "ROJO",     "label": "Crítico",         "color": "#FF4B4B", "emoji": "🔴", "max_wait_min": 0},
    2: {"name": "NARANJA",  "label": "Muy Urgente",     "color": "#FF8C00", "emoji": "🟠", "max_wait_min": 10},
    3: {"name": "AMARILLO", "label": "Urgente",         "color": "#FFD700", "emoji": "🟡", "max_wait_min": 60},
    4: {"name": "VERDE",    "label": "Poco Urgente",    "color": "#2ECC71", "emoji": "🟢", "max_wait_min": 120},
    5: {"name": "AZUL",     "label": "No Urgente",      "color": "#3498DB", "emoji": "🔵", "max_wait_min": 240},
}

TOTAL_BEDS = 10  # camas en urgencias


class HospitalTriageSystem:
    """
    Motor del sistema de triage.

    Estructuras usadas:
        - Array           → camas de urgencias (slots fijos)
        - Stack (Pila)    → historial de acciones (deshacer)
        - PriorityQueue   → cola de espera ordenada por prioridad
        - SinglyLinkedList→ log de eventos (auditoría)
        - DischargeList   → lista de pacientes dados de alta
    """

    def __init__(self):
        # --- Estructuras de datos ---
        self.beds = Array(TOTAL_BEDS)                   # ARRAY
        self.action_history = Stack()                   # PILA
        self.waiting_queue = PriorityQueue()            # COLA
        self.event_log = SinglyLinkedList()             # LISTA ENLAZADA SIMPLE
        self.discharged = DischargeList()               # LISTA

        # Pacientes activos en cama {bed_index: patient_dict}
        self.active_patients: dict = {}

        # Contador interno
        self._patient_counter = 0

    # ──────────────────────────────────────────
    # REGISTRO DE PACIENTE (ingresa a la cola)
    # ──────────────────────────────────────────
    def register_patient(self, name: str, age: int, symptoms: str, priority: int) -> dict:
        self._patient_counter += 1
        patient = {
            "id":        f"P{self._patient_counter:04d}",
            "name":      name,
            "age":       age,
            "symptoms":  symptoms,
            "priority":  priority,
            "triage":    TRIAGE_LEVELS[priority],
            "timestamp": time.time(),
            "registered_at": datetime.now().strftime("%H:%M:%S"),
            "status":    "En espera",
        }

        # → Cola de prioridad
        self.waiting_queue.enqueue(patient)

        # → Log de eventos (lista enlazada, al inicio = más reciente)
        self._log_event("REGISTRO", patient["id"], f"{name} ingresó — {TRIAGE_LEVELS[priority]['name']}")

        # → Pila de acciones (para deshacer)
        self.action_history.push({
            "action": "register",
            "patient_id": patient["id"],
            "patient": dict(patient),
        })

        return patient

    # ──────────────────────────────────────────
    # ASIGNAR CAMA (siguiente de la cola → cama libre)
    # ──────────────────────────────────────────
    def assign_bed(self, bed_index: int = None) -> dict | None:
        if self.waiting_queue.is_empty():
            return None

        free_slots = self.beds.available_slots()
        if not free_slots:
            return None

        # Elegir cama
        slot = bed_index if (bed_index is not None and bed_index in free_slots) else free_slots[0]

        # Sacar de la cola
        patient = self.waiting_queue.dequeue()
        patient["status"] = "En atención"
        patient["bed"] = slot
        patient["admitted_at"] = datetime.now().strftime("%H:%M:%S")
        patient["admit_timestamp"] = time.time()

        # → Array de camas
        self.beds.set(slot, patient["id"])
        self.active_patients[slot] = patient

        # → Log
        self._log_event("ASIGNACIÓN", patient["id"], f"Cama {slot + 1} asignada")

        # → Pila
        self.action_history.push({
            "action": "assign_bed",
            "patient_id": patient["id"],
            "bed_index": slot,
        })

        return patient

    # ──────────────────────────────────────────
    # DAR DE ALTA (libera cama → lista de altas)
    # ──────────────────────────────────────────
    def discharge_patient(self, bed_index: int, notes: str = "") -> dict | None:
        if self.beds.get(bed_index) is None:
            return None

        patient = self.active_patients.pop(bed_index, None)
        if not patient:
            return None

        patient["status"] = "Dado de alta"
        patient["discharge_time"] = time.time()
        patient["discharged_at"] = datetime.now().strftime("%H:%M:%S")
        patient["discharge_notes"] = notes

        # Calcular tiempo de estancia (minutos)
        if "admit_timestamp" in patient:
            stay = (patient["discharge_time"] - patient["admit_timestamp"]) / 60
            patient["stay_minutes"] = round(stay, 1)

        # Liberar cama en el Array
        self.beds.set(bed_index, None)

        # → Lista de altas
        self.discharged.add(patient)

        # → Log
        self._log_event("ALTA", patient["id"], f"Cama {bed_index + 1} liberada — {notes}")

        # → Pila
        self.action_history.push({
            "action": "discharge",
            "patient_id": patient["id"],
            "bed_index": bed_index,
        })

        return patient

    # ──────────────────────────────────────────
    # DESHACER última acción (Pila POP)
    # ──────────────────────────────────────────
    def undo_last_action(self) -> str:
        if self.action_history.is_empty():
            return "No hay acciones para deshacer."

        last = self.action_history.pop()
        action = last["action"]

        if action == "register":
            # Quitar de la cola
            self.waiting_queue.remove_by_id(last["patient_id"])
            self._log_event("DESHACER", last["patient_id"], "Registro cancelado")
            return f"Registro de {last['patient']['name']} cancelado."

        elif action == "assign_bed":
            bed = last["bed_index"]
            patient = self.active_patients.pop(bed, None)
            if patient:
                self.beds.set(bed, None)
                patient["status"] = "En espera"
                patient.pop("bed", None)
                patient.pop("admitted_at", None)
                self.waiting_queue.enqueue(patient)
                self._log_event("DESHACER", last["patient_id"], f"Cama {bed + 1} liberada (deshacer)")
                return f"Asignación de cama {bed + 1} deshecha. Paciente vuelve a la cola."
            return "No se encontró el paciente en la cama."

        elif action == "discharge":
            self._log_event("DESHACER", last["patient_id"], "Alta revertida (solo log)")
            return "Alta registrada en log — no se puede revertir completamente en esta versión."

        return "Acción desconocida."

    # ──────────────────────────────────────────
    # LOG (Lista Enlazada Simple)
    # ──────────────────────────────────────────
    def _log_event(self, event_type: str, patient_id: str, description: str):
        entry = {
            "time":        datetime.now().strftime("%H:%M:%S"),
            "type":        event_type,
            "patient_id":  patient_id,
            "description": description,
        }
        self.event_log.prepend(entry)  # más reciente al inicio

    # ──────────────────────────────────────────
    # ESTADÍSTICAS
    # ──────────────────────────────────────────
    def get_stats(self) -> dict:
        occupied = len(self.active_patients)
        return {
            "total_beds":     TOTAL_BEDS,
            "occupied_beds":  occupied,
            "free_beds":      TOTAL_BEDS - occupied,
            "waiting":        self.waiting_queue.size(),
            "discharged":     self.discharged.count(),
            "log_entries":    self.event_log.size(),
            "actions_stack":  self.action_history.size(),
        }

    def get_bed_status(self) -> list:
        """Devuelve estado de cada cama como lista de dicts."""
        result = []
        for i in range(TOTAL_BEDS):
            pid = self.beds.get(i)
            patient = self.active_patients.get(i)
            result.append({
                "bed":     i + 1,
                "status":  "Ocupada" if pid else "Libre",
                "patient": patient,
            })
        return result
