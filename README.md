# Notas KivyMD + JSON + notificación

Aplicación de escritorio hecha con **KivyMD 2.0** que guarda notas en un archivo
JSON y muestra una notificación del sistema al guardar.

## Características

- Campo de texto y botón **Guardar** (también funciona con `Enter`).
- Historial con la fecha de cada nota, la más reciente primero.
- Persistencia en `datos.app.json`: al abrir la app se recuperan las notas.
- Notificación nativa con `plyer`.
- Si el JSON no existe o está dañado, la app abre sin errores.

## Requisitos

- **Python 3.11** (probado con 3.11.1)
- Windows, Linux o macOS
- Dependencias: Kivy 2.3.1, KivyMD 2.0.0, plyer 2.1.0

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/NICOXDE123/Notificacion-kivy.git
cd Notificacion-kivy

# 2. Crear el entorno virtual
python -m venv myenv

# 3. Activarlo
# Windows:
myenv\Scripts\activate
# Linux / macOS:
source myenv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar
python main.py
```

## Uso

1. Escribe una nota en el campo de texto.
2. Pulsa **Guardar** o presiona `Enter`.
3. Aparece la notificación y la nota se agrega al historial con su fecha.
4. Cierra la app y vuelve a abrirla: las notas siguen ahí.

## Estructura del JSON

El archivo `datos.app.json` se guarda en la misma carpeta que `main.py`:

```json
{
    "notas": [
        {
            "texto": "ola",
            "fecha": "21/10/2026 21:30"
        }
    ]
}
```

- Al guardar se **reescribe el archivo completo** con la lista de notas, así que
  las anteriores no se pierden.
- Si el archivo no existe, se crea automáticamente al guardar la primera nota.

Puedes comprobar que el JSON es válido con:

```bash
python -m json.tool datos.app.json
```

## Estructura del proyecto

```
Notificacion-kivy/
├── main.py            # Lógica: JSON, historial y notificación
├── main.kv            # Interfaz (Kivy Language)
├── datos.app.json     # Notas guardadas
├── requirements.txt   # Dependencias con versiones fijas
├── README.md
└── .gitignore
```

## Nota sobre Android

La ruta del JSON usa la carpeta del proyecto, lo cual funciona en escritorio.
En Android la carpeta del APK es de solo lectura, así que habría que cambiar
`RUTA_JSON` para usar `self.user_data_dir`, y agregar `kivy, kivymd, plyer`
a los requisitos de Buildozer.

## Autor

Nicolas Huenchual Moreno .
