import cv2
import os

# ── Configuración ─────────────────────────────────────────────────────────────
carpeta = "fotos"
FOTOS_POR_DOCENTE = 5  # cantidad de fotos a capturar por docente

def hay_rostro(frame):
    """Detecta rostros con Haar Cascade. Retorna lista de rostros encontrados."""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(
        gris, scaleFactor=1.1, minNeighbors=6, minSize=(120, 120)
    )

# ── Setup ─────────────────────────────────────────────────────────────────────
os.makedirs(carpeta, exist_ok=True)

nombre = input("Nombre del docente: ").strip()
if not nombre:
    print("❌ Nombre vacío. Saliendo.")
    exit()

# Carpeta individual por docente
carpeta_docente = os.path.join(carpeta, nombre)
os.makedirs(carpeta_docente, exist_ok=True)

cap = cv2.VideoCapture(0)
fotos_tomadas = 0

print(f"\n📸 Se tomarán {FOTOS_POR_DOCENTE} fotos de {nombre}")
print("Presiona 'S' cuando tu rostro esté encuadrado | ESC para cancelar\n")

while fotos_tomadas < FOTOS_POR_DOCENTE:
    ret, frame = cap.read()
    if not ret:
        break

    rostros = hay_rostro(frame)

    # Dibuja rectángulo verde si detecta rostro válido
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Indicador de estado en pantalla
    if len(rostros) == 1:
        estado_txt = f"Rostro OK | Foto {fotos_tomadas + 1}/{FOTOS_POR_DOCENTE} | Presiona S"
        color = (0, 255, 0)
    elif len(rostros) > 1:
        estado_txt = "Mas de un rostro - solo uno a la vez"
        color = (0, 165, 255)
    else:
        estado_txt = "Sin rostro - Acercate a la camara"
        color = (0, 0, 255)

    cv2.putText(frame, estado_txt, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, f"Docente: {nombre}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Registro de Docente - Grupo 12", frame)
    key = cv2.waitKey(1)

    if key == ord('s') or key == ord('S'):
        if len(rostros) == 1:
            ruta = os.path.join(carpeta_docente, f"{nombre}_{fotos_tomadas + 1}.jpg")
            cv2.imwrite(ruta, frame)
            fotos_tomadas += 1
            print(f"  📷 Foto {fotos_tomadas}/{FOTOS_POR_DOCENTE} guardada -> {ruta}")
            if fotos_tomadas < FOTOS_POR_DOCENTE:
                print(f"  👉 Cambia ligeramente el angulo y presiona S de nuevo")
        else:
            print("  ❌ No se puede capturar: asegurate de que solo tu rostro este visible")

    elif key == 27:
        print("\n⚠️  Registro cancelado.")
        break

cap.release()
cv2.destroyAllWindows()

if fotos_tomadas == FOTOS_POR_DOCENTE:
    print(f"\n✅ Registro completo: {fotos_tomadas} fotos guardadas en '{carpeta_docente}/'")
else:
    print(f"\n⚠️  Registro incompleto: solo {fotos_tomadas}/{FOTOS_POR_DOCENTE} fotos guardadas")
