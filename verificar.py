import cv2
import os
from deepface import DeepFace
from datetime import datetime, time
import csv

# ── Configuración ─────────────────────────────────────────────────────────────
carpeta            = "fotos"
archivo_asistencia = "asistencia.csv"
HORA_ENTRADA       = time(7, 30, 0)   # Hora oficial de entrada
TOLERANCIA_MIN     = 10               # Minutos de tolerancia permitidos
UMBRAL_DISTANCIA   = 0.35             # Distancia coseno máxima (0.25=estricto, 0.40=permisivo)
VOTOS_NECESARIOS   = 2               # Mínimo de fotos que deben coincidir (de 5)

registrados_hoy = set()

# ── Funciones ─────────────────────────────────────────────────────────────────
def cargar_registrados_hoy():
    """Carga los nombres ya registrados hoy para evitar duplicados."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(archivo_asistencia):
        return
    with open(archivo_asistencia, "r", encoding="utf-8") as f:
        for fila in csv.reader(f):
            if len(fila) >= 2 and hoy in fila[1]:
                registrados_hoy.add(fila[0])

def estado_asistencia(hora_actual):
    """Clasifica el estado según HORA_ENTRADA y TOLERANCIA_MIN."""
    ahora_dt   = datetime.combine(datetime.today(), hora_actual)
    entrada_dt = datetime.combine(datetime.today(), HORA_ENTRADA)
    diff_min   = (ahora_dt - entrada_dt).total_seconds() / 60

    if diff_min <= 0:
        return "A TIEMPO"
    elif diff_min <= TOLERANCIA_MIN:
        return "TARDE (TOLERADO)"
    else:
        return "MUY TARDE"

def registrar(nombre):
    """Escribe el registro en el CSV si no existe duplicado hoy."""
    if nombre in registrados_hoy:
        print(f"⚠️  {nombre} ya fue registrado hoy.")
        return False

    ahora        = datetime.now()
    hora_formato = ahora.strftime("%Y-%m-%d %I:%M:%S %p")
    estado       = estado_asistencia(ahora.time())

    with open(archivo_asistencia, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([nombre, hora_formato, estado])

    registrados_hoy.add(nombre)
    print(f"✅ Registrado: {nombre} | {hora_formato} | {estado}")
    return True

def hay_rostro(frame):
    """Detecta rostros con Haar Cascade."""
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cascade.detectMultiScale(
        gris, scaleFactor=1.1, minNeighbors=6, minSize=(120, 120)
    )

def reconocer_docente(frame):
    """
    Reconocimiento con 3 capas de seguridad:
    1. Haar Cascade: debe haber exactamente 1 rostro
    2. DeepFace Facenet512: comparación por distancia coseno
    3. Sistema de votación: mínimo VOTOS_NECESARIOS fotos deben coincidir
    """
    # Capa 1: verificar exactamente 1 rostro
    rostros = hay_rostro(frame)
    if len(rostros) == 0:
        print("🚫 Sin rostro detectado")
        return None, "sin_rostro"
    if len(rostros) > 1:
        print("🚫 Multiples rostros detectados")
        return None, "multiples_rostros"

    temp_img = "temp.jpg"
    cv2.imwrite(temp_img, frame)

    mejor_nombre   = None
    mejor_promedio = float("inf")

    # Recorre subcarpetas: fotos/nombre/
    for docente in os.listdir(carpeta):
        ruta_docente = os.path.join(carpeta, docente)
        if not os.path.isdir(ruta_docente):
            continue

        votos      = 0
        distancias = []

        for archivo in os.listdir(ruta_docente):
            if not archivo.lower().endswith((".jpg", ".png")):
                continue

            ruta_foto = os.path.join(ruta_docente, archivo)
            try:
                resultado = DeepFace.verify(
                    img1_path         = temp_img,
                    img2_path         = ruta_foto,
                    model_name        = "Facenet512",
                    enforce_detection = False,
                    detector_backend  = "opencv",
                    distance_metric   = "cosine"
                )
                dist = resultado["distance"]
                distancias.append(dist)
                print(f"  {docente}/{archivo}: {dist:.4f}")

                if dist < UMBRAL_DISTANCIA:
                    votos += 1

            except Exception as e:
                print(f"  Error {docente}/{archivo}: {e}")

        print(f"  → {docente}: {votos}/{len(distancias)} votos")

        # Capa 3: sistema de votación
        if votos >= VOTOS_NECESARIOS and distancias:
            promedio = sum(distancias) / len(distancias)
            if promedio < mejor_promedio:
                mejor_promedio = promedio
                mejor_nombre   = docente

    if mejor_nombre:
        print(f"✅ Reconocido: {mejor_nombre} (dist prom={mejor_promedio:.4f})")
        return mejor_nombre, "ok"

    print(f"❌ No reconocido (mejor prom={mejor_promedio:.4f})")
    return None, "no_reconocido"

# ── Main ──────────────────────────────────────────────────────────────────────
os.makedirs(carpeta, exist_ok=True)
cargar_registrados_hoy()

cap     = cv2.VideoCapture(0)
mensaje = "Presiona V para verificar | ESC para salir"
color   = (255, 255, 255)

print("=" * 50)
print("  SISTEMA DE ASISTENCIA - GRUPO 12")
print("  I.E.P. La Cantuta Milenium")
print("=" * 50)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Rectángulo en tiempo real
    rostros = hay_rostro(frame)
    for (x, y, w, h) in rostros:
        col_rect = (0, 255, 0) if len(rostros) == 1 else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), col_rect, 2)

    if len(rostros) == 1:
        hint, hc = "Rostro OK - listo para verificar", (0, 255, 0)
    elif len(rostros) > 1:
        hint, hc = "Varios rostros - solo uno a la vez", (0, 165, 255)
    else:
        hint, hc = "Sin rostro detectado", (0, 0, 255)

    cv2.putText(frame, mensaje, (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, hint,    (10, 60),  cv2.FONT_HERSHEY_SIMPLEX, 0.55, hc,   2)
    cv2.imshow("Control de Asistencia - Grupo 12", frame)

    key = cv2.waitKey(1)

    if key in (ord('v'), ord('V')):
        mensaje = "Analizando..."
        color   = (0, 255, 255)

        nombre, estado = reconocer_docente(frame)

        if estado == "sin_rostro":
            mensaje, color = "Acerca tu rostro a la camara", (0, 0, 255)
        elif estado == "multiples_rostros":
            mensaje, color = "Solo un docente a la vez",     (0, 165, 255)
        elif estado == "no_reconocido":
            mensaje, color = "Docente no registrado",        (0, 0, 255)
        elif nombre:
            ok             = registrar(nombre)
            mensaje        = f"{nombre} registrado" if ok else f"{nombre} ya registrado hoy"
            color          = (0, 255, 0) if ok else (0, 165, 255)

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
