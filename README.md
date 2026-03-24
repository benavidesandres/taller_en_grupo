# 🏥 Sistema de Triage y Flujo de Sala de Urgencias

**Taller — Caso de Estudio | Frontend: Streamlit | Backend: Python**

---

## 📦 Instalación

```bash
pip install streamlit
streamlit run app.py
```

---

## 🗂️ Estructura del Proyecto

```
hospital_triage/
├── structures.py      ← Estructuras de datos puras
├── triage_system.py   ← Lógica de negocio
├── app.py             ← Frontend Streamlit
└── README.md
```

---

## 🧩 Estructuras de Datos Implementadas

| Estructura          | Clase             | Uso en el sistema                          | Complejidad clave         |
|---------------------|-------------------|--------------------------------------------|---------------------------|
| **Array**           | `Array`           | Camas de urgencias (10 slots fijos)        | `get/set` → O(1)          |
| **Pila (Stack)**    | `Stack`           | Historial de acciones → función "deshacer" | `push/pop` → O(1)         |
| **Cola (Queue)**    | `PriorityQueue`   | Pacientes en espera por prioridad (FIFO)   | `enqueue` → O(n log n)    |
| **Lista Enlazada**  | `SinglyLinkedList`| Log de eventos del sistema (audit trail)   | `prepend` → O(1)          |
| **Lista (Python)**  | `DischargeList`   | Registro de pacientes dados de alta        | `add` → O(1), `filter` O(n)|

---

## 🔄 Flujo del Sistema

```
Paciente llega
      │
      ▼
[REGISTRO] ──→ PriorityQueue.enqueue(paciente)
                     │ Cola ordenada por: prioridad → timestamp
                     ▼
[ASIGNAR CAMA] ──→ PriorityQueue.dequeue() → Array.set(slot, id)
                     │ Paciente pasa de "En espera" → "En atención"
                     ▼
[DAR DE ALTA] ──→ Array.set(slot, None) → DischargeList.add(paciente)
                     │ Cama liberada, paciente registrado en lista de altas

En cualquier momento:
  Stack.push(acción)  ← cada operación guarda contexto
  Stack.pop()         ← "deshacer" revierte la última acción
  SinglyLinkedList.prepend(evento) ← audit log siempre actualizado
```

---

## 🏥 Escala de Triage (Sistema Manchester)

| Nivel | Color     | Categoría    | Espera Máx. |
|-------|-----------|--------------|-------------|
| 1     | 🔴 Rojo   | Crítico      | 0 min       |
| 2     | 🟠 Naranja| Muy Urgente  | 10 min      |
| 3     | 🟡 Amarillo| Urgente     | 60 min      |
| 4     | 🟢 Verde  | Poco Urgente | 120 min     |
| 5     | 🔵 Azul   | No Urgente   | 240 min     |

---

## ✨ Funcionalidades

- ✅ Registro de pacientes con nivel de triage
- ✅ Cola de prioridad automática (nivel + tiempo)
- ✅ Asignación de camas (Array de slots fijos)
- ✅ Alta médica con notas y cálculo de estancia
- ✅ Historial de acciones con **deshacer** (Pila)
- ✅ Log de auditoría en tiempo real (Lista Enlazada)
- ✅ Registro histórico de altas (Lista Python)
- ✅ Dashboard de estadísticas en tiempo real
