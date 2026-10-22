import json
import os
from datetime import datetime

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from plyer import notification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# En Android habría que usar self.user_data_dir (la carpeta del APK no se escribe).
RUTA_JSON = os.path.join(BASE_DIR, "datos.app.json")
FORMATO_FECHA = "%d/%m/%Y %H:%M"


class NotasApp(MDApp):
    notas = []

    def build(self):
        return Builder.load_file(os.path.join(BASE_DIR, "main.kv"))

    def leer_notas(self):
        try:
            with open(RUTA_JSON, encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (OSError, json.JSONDecodeError) as error:
            if os.path.exists(RUTA_JSON):
                print("No se pudo leer el JSON:", error)
            return []

        notas = datos.get("notas", []) if isinstance(datos, dict) else []
        return [
            {"texto": nota["texto"], "fecha": nota.get("fecha", "")}
            for nota in notas
            if isinstance(nota, dict) and nota.get("texto")
        ]

    def guardar_notas(self):
        try:
            # "w" reescribe el archivo con la lista completa (no se pierde nada).
            with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
                json.dump({"notas": self.notas}, archivo,
                          ensure_ascii=False, indent=4)
            return True
        except OSError as error:
            print("No se pudo guardar el JSON:", error)
            return False

    def on_start(self):
        self.notas = self.leer_notas()
        self.actualizar_historial()

    def actualizar_historial(self):
        lista = self.root.ids.lista_notas
        lista.clear_widgets()

        for nota in self.notas:
            lista.add_widget(MDListItem(
                MDListItemHeadlineText(text=nota["texto"]),
                MDListItemSupportingText(text=nota["fecha"]),
            ))

        self.root.ids.titulo_historial.text = f"Historial ({len(self.notas)})"
        self.root.ids.mensaje_vacio.text = (
            "" if self.notas else "Todavía no hay notas guardadas."
        )

    def guardar_texto(self):
        texto = self.root.ids.campo_texto.text.strip()
        if not texto:
            return

        # La nota nueva va al principio, con la fecha actual.
        self.notas.insert(0, {
            "texto": texto,
            "fecha": datetime.now().strftime(FORMATO_FECHA),
        })
        if not self.guardar_notas():
            self.notas.pop(0)
            return

        self.actualizar_historial()
        self.root.ids.campo_texto.text = ""

        try:
            notification.notify(
                title="Guardado",
                message=f'El texto "{texto}" ha sido guardado exitosamente',
                app_name="Notas Kivy",
                timeout=5,
            )
        except Exception as error:
            print("No se pudo mostrar la notificación:", error)


if __name__ == "__main__":
    NotasApp().run()