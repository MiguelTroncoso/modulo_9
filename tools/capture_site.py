"""Genera las capturas del Kit de Empleabilidad Digital (Módulo 9).

Uso:
    python tools/capture_site.py

Levanta un servidor estático en el puerto 8098 y guarda las imágenes en
docs/screenshots/.
"""

import http.server
import os
import socketserver
import threading

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "docs", "screenshots")
PUERTO = 8098
BASE = f"http://127.0.0.1:{PUERTO}"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=RAIZ, **kwargs)

    def log_message(self, *args):
        pass


def capturar():
    os.makedirs(SALIDA, exist_ok=True)
    servidor = socketserver.TCPServer(("127.0.0.1", PUERTO), Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch(channel="chrome", headless=True)
            contexto = navegador.new_context(viewport={"width": 1440, "height": 940})
            pagina = contexto.new_page()
            pagina.goto(BASE, wait_until="networkidle")
            pagina.wait_for_timeout(1200)

            def shot(nombre, selector=None, full=False):
                if selector:
                    pagina.eval_on_selector(selector, "el => el.scrollIntoView({block:'start'})")
                    pagina.wait_for_timeout(800)
                pagina.screenshot(path=os.path.join(SALIDA, nombre), full_page=full)
                print("capturado:", nombre)

            shot("01_hero.png")
            shot("02_perfil.png", "#perfil")
            shot("03_plan.png", "#plan")
            shot("04_cv.png", "#cv")
            shot("05_linkedin.png", "#linkedin")
            shot("06_entrevistas.png", "#entrevistas")
            shot("07_banco_star.png", "#star")
            shot("08_pitch.png", "#pitch")
            shot("09_tracker.png", "#seguimiento")
            shot("10_plantillas.png", "#plantillas")
            shot("11_contacto.png", "#contacto")

            movil = navegador.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
            pm = movil.new_page()
            pm.goto(BASE, wait_until="networkidle")
            pm.wait_for_timeout(900)
            pm.screenshot(path=os.path.join(SALIDA, "12_movil.png"))
            print("capturado: 12_movil.png")
            navegador.close()
    finally:
        servidor.shutdown()


if __name__ == "__main__":
    capturar()
    print("Listo ->", SALIDA)
