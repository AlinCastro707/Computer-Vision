import os
import time
from deepface import DeepFace

#perfiles del hogar para los usuarios autorizados
PERFILES_SMART_HOME = {
    "alin": {
        "musica": "Reproduciendo: Malice Mizer",
        "luces": "Luces reguladas a azul neón retro (Brillo 40%) ",
        "temperatura": "Aire acondicionado fijado en 22°C "
    },
    "mama": {
        "musica": "Reproduciendo: Éxitos de los 80s",
        "luces": "Luces encendidas en modo Cálido (Brillo 80%)",
        "temperatura": "Climatización a 24°C"
    }
}

def ejecutar_perfil_hogar(nombre_usuario):
    """Simula la activación de las preferencias físicas de la casa"""
    print(f"\n[Smart Home] ¡Bienvenido a casa, {nombre_usuario.capitalize()}!")
    perfil = PERFILES_SMART_HOME.get(nombre_usuario.lower())
    
    if perfil:
        time.sleep(1)
        print(f"  └─> {perfil['musica']}")
        time.sleep(1)
        print(f"  └─> {perfil['luces']}")
        time.sleep(1)
        print(f"  └─> {perfil['temperatura']}")
    else:
        print("  └─> Cargando perfil predeterminado de invitado.")

# La logica de verificacion facial
def intentar_inicio_sesion(ruta_foto_intento):
    print("\n" + "="*60)
    print(f"🔍 Escaneando rostro de origen: '{ruta_foto_intento}'...")
    print("="*60)
    
    carpeta_bd = "base_datos"
    usuario_autenticado = None
    
    # Recorremos las fotos
    for archivo in os.listdir(carpeta_bd):
        if archivo.endswith(('.jpg', '.jpeg', '.png')):
            ruta_foto_bd = os.path.join(carpeta_bd, archivo)
            nombre_usuario = os.path.splitext(archivo)[0] # Obtiene el nombre sin el .jpg
            
            try:
                # Comparamos de manera matematica ambos rostros mediante DeepFace
                resultado = DeepFace.verify(
                    img1_path=ruta_foto_intento, 
                    img2_path=ruta_foto_bd, 
                    enforce_detection=False # Evita que el script muera si la foto no está perfectamente centrada
                )
                
                if resultado["verified"]:
                    usuario_autenticado = nombre_usuario
                    break # Si ya encontramos coincidencia, salimos del ciclo
                    
            except Exception as e:
                print(f"[ERROR] No se pudo procesar la comparación con {archivo}: {e}")

    #control de acceso
    if usuario_autenticado:
        print(f"[ACCESO CONCEDIDO] Rostro verificado con éxito.")
        print(f"Sesión iniciada como: USER_{usuario_autenticado.upper()}")
        # Disparamos la acción del proyecto 3
        ejecutar_perfil_hogar(usuario_autenticado)
    else:
        print("[ACCESO DENEGADO] Rostro desconocido. Alerta de seguridad enviada.")
        print("[Smart Home] Manteniendo puertas cerradas y luces de alarma activas.")

#flujo principal
if __name__ == "__main__":
    print("--- INICIANDO SISTEMA BIOMÉTRICO INTEGRADO ---")
    
    # Asegurémonos de que las carpetas existen antes de correr el script
    if not os.path.exists("base_datos") or not os.listdir("base_datos"):
        print("Alerta: Recuerda poner fotos en la carpeta 'base_datos' antes de ejecutar.")
    else:
        #Alguien autorizado intenta ingresar
        foto_exito = os.path.join("intentos_login", "login_exito.jpg")
        if os.path.exists(foto_exito):
            intentar_inicio_sesion(foto_exito)
            
        # Alguien sin autorización intenta ingresar
        foto_intruso = os.path.join("intentos_login", "login_intruso.jpg")
        if os.path.exists(foto_intruso):
            time.sleep(2)
            intentar_inicio_sesion(foto_intruso)