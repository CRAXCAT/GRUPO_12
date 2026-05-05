# 🎓 Sistema de Control de Asistencia Docente mediante Reconocimiento Facial
### GRUPO 12 — Arquitectura de Software
![Descripción de la imagen](https://raw.githubusercontent.com/CRAXCAT/GRUPO_12/refs/heads/main/fotos/Benjamin/Benjamin_1.jpg)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![DeepFace](https://img.shields.io/badge/DeepFace-Facenet512-orange)
![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow)

---

## 👥 Integrantes

| N° | Apellidos y Nombres |
|----|---------------------|
| 1 | Oyola Gutierrez, Jerzeell Juniors |
| 2 | Ccente Garcia, Kevin |
| 3 | Tovar Montoya, Benjamin Joaquin |

**Docente:** Mg. Raúl Enrique Fernández Bejarano  
**Curso:** Arquitectura de Software  
**Ciclo:** VIII — 2026  
**Institución objetivo:** I.E.P. La Cantuta Milenium — Huancayo, Perú

---

## 📌 Descripción del Proyecto

Sistema de control de asistencia para docentes de la I.E.P. La Cantuta Milenium que reemplaza el registro manual mediante **reconocimiento facial en tiempo real**, utilizando Python, OpenCV y DeepFace.

El sistema clasifica automáticamente la asistencia en:
- 🟢 **A TIEMPO** — marca antes o en la hora exacta de entrada
- 🟡 **TARDE (TOLERADO)** — dentro del margen de tolerancia configurado
- 🔴 **MUY TARDE** — supera el límite de tolerancia

---

## 🛠️ Tecnologías Utilizadas

| Librería | Versión | Uso |
|----------|---------|-----|
| Python | 3.x | Lenguaje principal |
| OpenCV (cv2) | 4.x | Captura de video y detección Haar Cascade |
| DeepFace | Latest | Reconocimiento facial con Facenet512 |
| CSV / datetime | Stdlib | Persistencia y cálculo de estados |
| os | Stdlib | Gestión de carpetas del padrón facial |

---

## 📁 Estructura del Proyecto

```
grupo12-asistencia-facial/
│
├── registrar.py          # Módulo de enrolamiento facial
├── verificar.py          # Módulo de marcaje diario
├── asistencia.csv        # Registro de asistencias (generado automáticamente)
│
├── fotos/                # Padrón fotográfico por docente
│   ├── benjamin/
│   │   ├── benjamin_1.jpg
│   │   ├── benjamin_2.jpg
│   │   └── ...
│   └── [nombre_docente]/
│       └── ...
│
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo
```

---

## ⚙️ Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/[usuario]/grupo12-asistencia-facial.git
cd grupo12-asistencia-facial
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Registrar un docente (una sola vez por docente)
```bash
python registrar.py
```
> Ingresa el nombre del docente → posiciona el rostro → presiona **S** 5 veces desde distintos ángulos.

### 4. Iniciar el control de asistencia (uso diario)
```bash
python verificar.py
```
> Posiciona el rostro frente a la cámara → presiona **V** para verificar → el sistema clasifica y registra automáticamente.

---

## 🔧 Configuración

Edita las constantes al inicio de `verificar.py`:

```python
HORA_ENTRADA     = time(7, 30, 0)   # Hora oficial de entrada
TOLERANCIA_MIN   = 10               # Minutos de tolerancia
UMBRAL_DISTANCIA = 0.35             # Sensibilidad (0.25 = estricto, 0.40 = permisivo)
VOTOS_NECESARIOS = 2                # Mínimo de fotos que deben coincidir (de 5)
```

---

## 📊 Requerimientos Funcionales Implementados

| Código | Requerimiento | Estado |
|--------|--------------|--------|
| RF-001 | Reconocimiento facial con DeepFace + Facenet512 | ✅ Completo |
| RF-002 | Clasificación automática A TIEMPO / TARDE / MUY TARDE | ✅ Completo |
| RF-003 | Registro en archivo CSV con fecha-hora AM/PM | ✅ Completo |
| RF-004 | Enrolamiento facial con 5 fotos por docente | ✅ Completo |
| RF-005 | Validación previa de rostro con Haar Cascade | ✅ Completo |
| RF-006 | Sistema de votación anti-falsos positivos | ✅ Completo |
| RF-007 | Retroalimentación visual en tiempo real | ✅ Completo |
| RF-008 | Estructura de carpetas por docente | ✅ Completo |
| RF-009 | Stack Python sin GPU requerida | ✅ Completo |
| RF-010 | Prevención de registros duplicados diarios | ✅ Completo |
| RF-011 | Parámetros configurables centralizados | ✅ Completo |
| RF-012 | Módulos independientes registrar / verificar | ✅ Completo |

---

## 🚀 Avance del Proyecto (Metodología XP)

| Iteración | Módulo | Estado |
|-----------|--------|--------|
| Iter. 1 | `registrar.py` — Enrolamiento facial básico | ✅ Completado |
| Iter. 2 | `verificar.py` — Reconocimiento + CSV + estados | ✅ Completado |
| Iter. 3 | Anti-falsos positivos + sistema de votación | ✅ Completado |
| Iter. 4 | Reportes / Historial / Justificaciones | 🔄 Pendiente |

---

## 📄 Formato del archivo asistencia.csv

```
Nombre,FechaHora,Estado
benjamin,2026-05-03 07:28:15 AM,A TIEMPO 🟢
kevin,2026-05-03 07:41:03 AM,TARDE 🟡 (TOLERADO)
jerzeell,2026-05-03 08:05:22 AM,MUY TARDE 🔴
```

---

## 📝 Licencia

Proyecto académico — Universidad Peruana Los Andes  
Facultad de Ingeniería — Escuela de Ingeniería de Sistemas y Computación  
**© 2026 Grupo 12**
