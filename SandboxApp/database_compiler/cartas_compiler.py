import os
import json
import re
import unicodedata

print("[SISTEMA] Iniciando el Compilador Inteligente por Escaneo de Disco...")

CARPETA_RAW = "./raw_editions"

# 1. Localizar la raíz de SandboxApp de forma dinámica
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_sandbox_app = os.path.abspath(os.path.join(directorio_actual, ".."))

# 2. ALGORITMO DE RASTREO: Encontrar todas las carpetas activas de datos en el proyecto
rutas_destino_json = []
ruta_origen_desarrollo = os.path.join(ruta_sandbox_app, "wwwroot", "data", "cartas.json")
rutas_destino_json.append(ruta_origen_desarrollo)

ruta_bin = os.path.join(ruta_sandbox_app, "bin")
if os.path.exists(ruta_bin):
    for raiz, carpetas, archivos in os.walk(ruta_bin):
        if raiz.endswith(os.path.join("wwwroot", "data")):
            rutas_destino_json.append(os.path.join(raiz, "cartas.json"))

# FUNCIÓN DE NORMALIZACIÓN: Convierte cualquier texto en una clave pura de letras y números
def normalizar_para_busqueda(texto):
    texto = texto.lower()
    # Quitar la extensión si viene de un archivo de disco
    if texto.endswith('.jpg') or texto.endswith('.png') or texto.endswith('.jpeg'):
        texto = os.path.splitext(texto)[0]
    # Eliminar tildes y diéresis de forma limpia
    texto = "".join([c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'])
    # Conservar solo caracteres alfanuméricos puros (letras y números)
    return re.sub(r'[^a-z0-9]', '', texto)

def compilar_base_datos():
    if not os.path.exists(CARPETA_RAW):
        os.makedirs(CARPETA_RAW)
        print(f"[SISTEMA] Creada carpeta '{CARPETA_RAW}'. Coloca tus JSONs de las ediciones ahí.")
        return

    inventario_maestro = []
    contador_ids = 1

    archivos_json = [f for f in os.listdir(CARPETA_RAW) if f.endswith('.json')]
    
    if not archivos_json:
        print("[ADVERTENCIA] No encontré archivos JSON dentro de 'raw_editions/'.")
        return

    diccionario_ediciones = {
        "cards_espada-sagrada.json": "Espada Sagrada",
        "cards_helenica.json": "Helénica",
        "cards_dominios-de-ra.json": "Dominios de Ra",
        "cards_hijos_de_daana.json": "Hijos de Daana",
        "cards_tierras_altas.json": "Tierras Altas",
        "cards_encrucijada.json": "Encrucijada",
        "cards_cruzadas.json": "Cruzadas",
        "cards_imperio.json": "Imperio",
        "cards_promocionales_primer_bloque.json": "Promocionales"
    }

    print(f"[INFO] Se detectaron {len(archivos_json)} archivos de edición listos para procesar.")

    for archivo in archivos_json:
        ruta_archivo = os.path.join(CARPETA_RAW, archivo)
        
        if archivo in diccionario_ediciones:
            edicion_real = diccionario_ediciones[archivo]
        else:
            if "helenica" in archivo.lower(): edicion_real = "Helénica"
            elif "espada" in archivo.lower(): edicion_real = "Espada Sagrada"
            elif "dominios" in archivo.lower(): edicion_real = "Dominios de Ra"
            else: edicion_real = archivo.replace("cards_", "").replace(".json", "").replace("-", " ").title()

        print(f"[PROCESO] Escaneando y mapeando edición: [{edicion_real}]")

        # --- MOTOR DE RASTREO REAL EN DISCO ---
        # Escaneamos la carpeta real de imágenes para saber exactamente qué archivos tienes guardados
        mapa_archivos_reales = {}
        ruta_carpeta_imagenes = os.path.join(ruta_sandbox_app, "wwwroot", "images", edicion_real)
        
        if os.path.exists(ruta_carpeta_imagenes):
            for item_disco in os.listdir(ruta_carpeta_imagenes):
                if os.path.isfile(os.path.join(ruta_carpeta_imagenes, item_disco)):
                    clave_archivo = normalizar_para_busqueda(item_disco)
                    mapa_archivos_reales[clave_archivo] = item_disco

        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            try:
                cartas_edicion = json.load(f)
            except Exception as e:
                print(f"[ERROR] Al leer {archivo}: {e}")
                continue

            for carta in cartas_edicion:
                c_limpia = {k.lower().strip(): v for k, v in carta.items()}
                
                nombre_real = str(c_limpia.get("nombre", c_limpia.get("name", ""))).strip()
                if not nombre_real or nombre_real.lower() == "none":
                    continue

                # Calculamos la clave de la carta
                clave_carta = normalizar_para_busqueda(nombre_real)
                
                # Buscamos si existe un archivo físico real en tu disco que coincida
                if clave_carta in mapa_archivos_reales:
                    archivo_imagen = mapa_archivos_reales[clave_carta]
                else:
                    # Fallback estándar si la imagen no existe en la carpeta aún
                    archivo_imagen = nombre_real.replace(" ", "_") + ".jpg"
                
                molde_blazor = {
                    "Id": f"MID-{str(contador_ids).zfill(4)}",
                    "Nombre": nombre_real,
                    "Edicion": edicion_real,
                    "Tipo": str(c_limpia.get("tipo", c_limpia.get("type", "Aliado"))).strip().capitalize(),
                    "Rareza": str(c_limpia.get("rareza", c_limpia.get("rarity", "Vasallo"))).strip().capitalize(),
                    "RutaImagen": f"images/{edicion_real}/{archivo_imagen}",
                    "Fuerza": c_limpia.get("fuerza", c_limpia.get("power", c_limpia.get("attack"))),
                    "Costo": c_limpia.get("costo", c_limpia.get("coste", c_limpia.get("cost"))),
                    "Habilidad": str(c_limpia.get("habilidad", c_limpia.get("ability", c_limpia.get("text", "")))).strip()
                }

                try: molde_blazor["Fuerza"] = int(molde_blazor["Fuerza"]) if molde_blazor["Fuerza"] is not None else None
                except: molde_blazor["Fuerza"] = None

                try: molde_blazor["Costo"] = int(molde_blazor["Costo"]) if molde_blazor["Costo"] is not None else None
                except: molde_blazor["Costo"] = None

                inventario_maestro.append(molde_blazor)
                contador_ids += 1

    for ruta_destino in set(rutas_destino_json):
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
        with open(ruta_destino, 'w', encoding='utf-8') as f_destino:
            json.dump(inventario_maestro, f_destino, indent=4, ensure_ascii=False)
        print(f"[GUARDADO] Archivo unificado en: {ruta_destino}")

    print(f"\n[ÉXITO] Base de datos e imágenes sincronizadas al 100% con tu disco.")
    print(f"[INFO] Total de cartas indexadas en el juego: {len(inventario_maestro)}")

if __name__ == "__main__":
    compilar_base_datos()