"""Genera el CV de una página de Miguel Troncoso para el portafolio (Módulo 8).

Uso:
    python tools/build_cv_pdf.py

Salida: docs/CV_Miguel_Troncoso.pdf
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, "docs")
SALIDA = os.path.join(DOCS, "CV_Miguel_Troncoso.pdf")

INK = colors.HexColor("#0b1120")
ACCENT = colors.HexColor("#0f9d76")
ACCENT_2 = colors.HexColor("#2f6fd6")
BODY = colors.HexColor("#1f2a37")
MUTED = colors.HexColor("#5b6b82")
LINE = colors.HexColor("#d7dee9")

CONTACTO = (
    "Santiago, Chile (remoto)  |  miguel.troncoso36@gmail.com  |  github.com/MiguelTroncoso  |  "
    "linkedin.com/in/miguel-troncoso  |  migueltroncoso.github.io/modulo_8"
)


def estilos():
    return {
        "nombre": ParagraphStyle("nombre", fontName="Helvetica-Bold", fontSize=24, leading=27,
                                 textColor=INK, spaceAfter=2),
        "rol": ParagraphStyle("rol", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                              textColor=ACCENT, spaceAfter=3),
        "contacto": ParagraphStyle("contacto", fontName="Helvetica", fontSize=8.6, leading=12,
                                   textColor=MUTED),
        "sec": ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                              textColor=ACCENT_2, spaceBefore=11, spaceAfter=5),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=13.4,
                               textColor=BODY, alignment=4, spaceAfter=3),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.4, leading=13.2,
                                 textColor=BODY, leftIndent=11, bulletIndent=1, spaceAfter=3),
        "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.3, leading=12.6,
                                textColor=INK),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.3, leading=12.6,
                               textColor=BODY),
    }


def construir():
    os.makedirs(DOCS, exist_ok=True)
    E = estilos()
    doc = SimpleDocTemplate(
        SALIDA, pagesize=A4, leftMargin=42, rightMargin=42, topMargin=40, bottomMargin=36,
        title="CV - Miguel Troncoso", author="Miguel Troncoso",
        subject="Curriculum Vitae - Desarrollador Web Junior",
    )
    ancho = A4[0] - 84
    s = [Paragraph("Miguel Troncoso", E["nombre"]),
         Paragraph("Desarrollador Web Junior &nbsp;|&nbsp; Python · Django · SQL", E["rol"]),
         Paragraph(CONTACTO, E["contacto"]),
         Spacer(1, 6), HRFlowable(width="100%", thickness=1, color=LINE)]

    s.append(Paragraph("Perfil profesional", E["sec"]))
    s.append(Paragraph(
        "Desarrollador web junior con foco en backend, formado en un bootcamp intensivo de desarrollo "
        "de software. Construyo aplicaciones con Python y Django: modelo de datos, lógica de negocio, "
        "CRUD, autenticación y pruebas automatizadas. Me interesa la integridad de los datos, la "
        "calidad del código y la documentación técnica.", E["body"]))

    s.append(Paragraph("Habilidades técnicas", E["sec"]))
    habilidades = [
        ("Lenguajes", "Python 3, SQL, HTML5, CSS3, JavaScript (básico)."),
        ("Frameworks", "Django 6 (ORM, vistas basadas en clases, admin, auth), Flask, Bootstrap 5."),
        ("Bases de datos", "SQLite, PostgreSQL, modelado relacional, migraciones y consultas ORM (raw y cursores)."),
        ("Herramientas", "Git, GitHub, Visual Studio Code, Django TestCase, unittest, Playwright."),
        ("Prácticas", "Testing automatizado, trabajo por ramas, documentación técnica y seguridad CSRF."),
    ]
    filas = [[Paragraph(k, E["cellb"]), Paragraph(v, E["cell"])] for k, v in habilidades]
    t = Table(filas, colWidths=[95, ancho - 95])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
    ]))
    s.append(t)

    s.append(Paragraph("Proyectos destacados", E["sec"]))
    proyectos = [
        ("Alke Wallet (Módulo 7)",
         "Billetera digital en Django con relaciones 1:1, 1:N y M:N, actualización atómica de saldos "
         "y 36 pruebas automatizadas. Python, Django, SQLite/PostgreSQL."),
        ("TaskMaster (Módulo 6)",
         "Plataforma de gestión de proyectos y tareas con autenticación, permisos por usuario y "
         "dashboard de indicadores; 18 pruebas automatizadas. Python, Django, Bootstrap."),
        ("ClickAndGo (Módulo 5)",
         "E-commerce de consola con persistencia SQLite, arquitectura por capas (DAO y servicios), "
         "integración con la API del dólar y guion de pruebas P01-P19. Python, SQLite, Flask."),
    ]
    for nombre, desc in proyectos:
        s.append(Paragraph(f"<b>{nombre}</b> · {desc}", E["bullet"], bulletText="\u2022"))

    s.append(Paragraph("Formación", E["sec"]))
    s.append(Paragraph(
        "<b>Bootcamp de Desarrollo de Aplicaciones Web (2026).</b> Formación intensiva en "
        "fundamentos de programación con Python, bases de datos relacionales, desarrollo web con "
        "Django (ORM, migraciones, CRUD y aplicaciones preinstaladas) y construcción de portafolio "
        "profesional.", E["body"]))

    s.append(Paragraph("Idiomas", E["sec"]))
    s.append(Paragraph("Español: nativo. &nbsp; Inglés: lectura técnica básica/intermedia.", E["body"]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=0.8, color=LINE))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Portafolio con caso de estudio técnico: migueltroncoso.github.io/modulo_8", E["contacto"]))

    doc.build(s)
    return SALIDA


if __name__ == "__main__":
    print("CV generado:", construir())
