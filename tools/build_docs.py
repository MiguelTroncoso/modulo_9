"""Genera los documentos PDF del Módulo 9 (empleabilidad).

Uso:
    python tools/build_docs.py

Salidas:
    docs/Plan_Busqueda_Laboral_Miguel_Troncoso.pdf
    docs/Guia_Entrevistas_Miguel_Troncoso.pdf
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, "docs")

INK = colors.HexColor("#0b0f1f")
INK_2 = colors.HexColor("#1a2440")
ACCENT = colors.HexColor("#5b3df0")
ACCENT_2 = colors.HexColor("#0e7c9b")
SUCCESS = colors.HexColor("#0f9d76")
BODY = colors.HexColor("#1f2a37")
MUTED = colors.HexColor("#5b6b82")
LINE = colors.HexColor("#d7dee9")
SURFACE = colors.HexColor("#f4f6fb")

TITULO_PLAN = "Plan de Búsqueda Laboral"
TITULO_ENTREVISTAS = "Guía de Entrevistas y Banco STAR"
SUBTITULO = "Miguel Troncoso · Desarrollador Web Junior (Python · Django · SQL)"


def estilos():
    base = getSampleStyleSheet()
    e = {
        "doc": ParagraphStyle("doc", parent=base["Title"], fontName="Helvetica-Bold",
                              fontSize=22, leading=26, textColor=INK, alignment=TA_LEFT, spaceAfter=2),
        "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=10.5, leading=14,
                              textColor=MUTED, spaceAfter=2),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19,
                             textColor=INK, spaceBefore=14, spaceAfter=6),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                             textColor=ACCENT, spaceBefore=12, spaceAfter=5),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.8,
                               textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=6),
        "lead": ParagraphStyle("lead", fontName="Helvetica", fontSize=10.6, leading=15.4,
                               textColor=MUTED, spaceAfter=8),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.6, leading=12,
                                textColor=MUTED, alignment=TA_LEFT),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.8, leading=14,
                                 textColor=BODY, leftIndent=12, bulletIndent=1, spaceAfter=3),
        "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.1, leading=12.4,
                                textColor=INK),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.1, leading=12.4,
                               textColor=BODY, alignment=TA_LEFT),
        "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=9.2, leading=12.4,
                                textColor=colors.white),
        "metric": ParagraphStyle("metric", fontName="Helvetica-Bold", fontSize=15, leading=18,
                                 textColor=ACCENT, alignment=TA_CENTER, spaceAfter=1),
        "metricc": ParagraphStyle("metricc", fontName="Helvetica", fontSize=8.2, leading=11.4,
                                  textColor=MUTED, alignment=TA_CENTER),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=8, leading=11.4,
                               textColor=colors.HexColor("#0b3a4a"), alignment=TA_LEFT),
    }
    return e


E = estilos()


def p(texto, estilo="body"):
    return Paragraph(texto, E[estilo])


def vineta(texto):
    return Paragraph(texto, E["bullet"], bulletText="\u2022")


def tabla(filas, anchos, encabezado=True):
    t = Table(filas, colWidths=anchos, repeatRows=1 if encabezado else 0)
    estilo = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.7, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    if encabezado:
        estilo += [
            ("BACKGROUND", (0, 0), (-1, 0), INK_2),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SURFACE]),
        ]
    else:
        estilo.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, SURFACE]))
    t.setStyle(TableStyle(estilo))
    return t


def caja_datos(datos):
    """Fila de indicadores: lista de tuplas (valor, etiqueta)."""
    cabecera = [p(v, "metric") for v, _ in datos]
    pie = [p(e, "metricc") for _, e in datos]
    ancho = (A4[0] - 96) / float(len(datos))
    t = Table([cabecera, pie], colWidths=[ancho] * len(datos))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.7, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def encabezado_pie(titulo):
    def _draw(canvas, doc):
        ancho, alto = A4
        canvas.saveState()
        canvas.setFillColor(ACCENT)
        canvas.rect(0, alto - 10, ancho, 10, stroke=0, fill=1)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(48, 34, "Miguel Troncoso - " + titulo)
        canvas.drawRightString(ancho - 48, 34, "Pagina %d" % doc.page)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.6)
        canvas.line(48, 46, ancho - 48, 46)
        canvas.restoreState()
    return _draw


def bloque_titulo(titulo, bajada):
    contenido = [
        p(titulo, "doc"),
        p(SUBTITULO, "sub"),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=1.2, color=ACCENT),
        Spacer(1, 10),
        p(bajada, "lead"),
    ]
    return contenido


# --------------------------------------------------------------------------
# Documento 1: Plan de búsqueda laboral
# --------------------------------------------------------------------------
def construir_plan():
    ruta = os.path.join(DOCS, "Plan_Busqueda_Laboral_Miguel_Troncoso.pdf")
    doc = SimpleDocTemplate(ruta, pagesize=A4, leftMargin=48, rightMargin=48,
                            topMargin=52, bottomMargin=58,
                            title="Plan de Busqueda Laboral - Miguel Troncoso",
                            author="Miguel Troncoso")
    ancho = A4[0] - 96
    s = bloque_titulo(
        TITULO_PLAN,
        "Plan de acción para conseguir una primera oportunidad como desarrollador junior "
        "en la industria tecnológica. Incluye objetivo, dedicación, puestos y empresas objetivo, "
        "canales de publicación, estrategia de LinkedIn, métricas y seguimiento.",
    )

    s.append(caja_datos([
        ("4 meses", "Plazo objetivo"),
        ("20 h", "Dedicación semanal"),
        ("10", "Postulaciones/semana"),
        ("80", "Postulaciones totales"),
    ]))

    s.append(p("1. Objetivo de búsqueda", "h2"))
    s.append(p(
        "Conseguir un puesto de <b>desarrollador backend o web junior</b> en una empresa "
        "tecnológica de Chile, en modalidad remota o híbrida, durante los próximos cuatro meses, "
        "postulando de forma constante y sostenida a ofertas alineadas a Python, Django y SQL."))
    s.append(vineta("<b>Corto plazo (0-1 mes):</b> CV, LinkedIn y portafolio publicados, revisados y enlazados entre sí."))
    s.append(vineta("<b>Mediano plazo (2-3 meses):</b> 80 postulaciones enviadas y al menos 4 entrevistas realizadas."))
    s.append(vineta("<b>Largo plazo (4 meses):</b> una oferta junior o trainee aceptada."))

    s.append(p("2. Dedicación semanal", "h2"))
    s.append(tabla(
        [[p("Bloque", "cellh"), p("Horario", "cellh"), p("Actividad", "cellh")],
         [p("Lunes a viernes", "cellb"), p("09:00 - 11:00", "cell"), p("Búsqueda, postulaciones y ajuste del CV", "cell")],
         [p("Martes y jueves", "cellb"), p("11:00 - 13:00", "cell"), p("Estudio técnico y práctica de código", "cell")],
         [p("Viernes", "cellb"), p("11:00 - 12:00", "cell"), p("Networking y actividad en LinkedIn", "cell")],
         [p("Sábado", "cellb"), p("10:00 - 12:00", "cell"), p("Simulación de entrevistas y práctica del pitch", "cell")]],
        [110, 95, ancho - 205],
    ))
    s.append(Spacer(1, 4))
    s.append(p("Total: 20 horas semanales dedicadas a la búsqueda y a la preparación.", "small"))

    s.append(p("3. Puestos objetivo", "h2"))
    s.append(tabla(
        [[p("Puesto", "cellh"), p("Tecnologías", "cellh"), p("Prioridad", "cellh")],
         [p("Desarrollador Backend Junior", "cellb"), p("Python, Django, ORM, APIs, PostgreSQL", "cell"), p("Alta", "cell")],
         [p("Desarrollador Web Junior", "cellb"), p("Django, HTML, CSS, Bootstrap, JavaScript", "cell"), p("Alta", "cell")],
         [p("Trainee / Analista Programador", "cellb"), p("Python, SQL, soporte al desarrollo", "cell"), p("Media", "cell")],
         [p("QA / Soporte con proyección", "cellb"), p("Testing, SQL, gestión de incidencias", "cell"), p("Alternativa", "cell")]],
        [180, ancho - 260, 80],
    ))

    s.append(PageBreak())
    s.append(p("4. Empresas objetivo", "h2"))
    s.append(p(
        "Seleccioné empresas reales del ecosistema tecnológico chileno cuyo perfil técnico se "
        "alinea con mi stack y con el tipo de problema que quiero resolver.", "body"))
    s.append(tabla(
        [[p("Empresa", "cellh"), p("Por qué me interesa", "cellh")],
         [p("Fintual", "cellb"), p("Fintech chilena con uso intensivo de Python y foco en datos financieros.", "cell")],
         [p("Buk", "cellb"), p("SaaS de recursos humanos con equipos de producto consolidados.", "cell")],
         [p("Defontana", "cellb"), p("Software de gestión chileno con desarrollo de producto propio.", "cell")],
         [p("Xepelin / Chipax", "cellb"), p("Fintech B2B que trabajan con datos, integraciones y servicios web.", "cell")],
         [p("Betterfly", "cellb"), p("Welltech con crecimiento regional y equipos de ingeniería.", "cell")],
         [p("Banca y retail tech", "cellb"), p("Banco de Chile, BancoEstado y Falabella: transformación digital a gran escala.", "cell")],
         [p("Startups GetOnBoard", "cellb"), p("Ofertas tech remotas con procesos de selección ágiles.", "cell")],
         [p("Consultoras TI", "cellb"), p("Puerta de entrada frecuente para perfiles trainee y junior.", "cell")]],
        [150, ancho - 150],
    ))

    s.append(p("5. Canales y portales", "h2"))
    s.append(tabla(
        [[p("Canal", "cellh"), p("Uso que le doy", "cellh")],
         [p("LinkedIn Jobs", "cellb"), p("Alertas con búsquedas booleanas y postulación directa.", "cell")],
         [p("GetOnBoard", "cellb"), p("Portal exclusivo de la industria tecnológica.", "cell")],
         [p("Laborum", "cellb"), p("Filtros por zona, nivel de experiencia y tipo de contratación.", "cell")],
         [p("FirstJob", "cellb"), p("Ofertas para 0-2 años de experiencia, prácticas y pasantías.", "cell")],
         [p("Trabajando.com / Indeed", "cellb"), p("Volumen de ofertas y alertas por correo.", "cell")],
         [p("Portales de empresa", "cellb"), p("Postulación espontánea con correo personalizado.", "cell")],
         [p("Red de contacto", "cellb"), p("Docentes, compañeros y referidos internos.", "cell")]],
        [165, ancho - 165],
    ))

    s.append(PageBreak())
    s.append(p("6. LinkedIn y estrategia de difusión", "h2"))
    s.append(p("<b>Titular:</b> Desarrollador Backend Junior | Python - Django - SQL | Construyo "
               "aplicaciones web con datos íntegros"))
    s.append(p("<b>Resumen:</b> Desarrollador web junior con foco en backend. Construyo aplicaciones "
               "con Python y Django: modelo de datos, lógica de negocio, CRUD, autenticación y pruebas "
               "automatizadas. Me interesa la integridad de los datos y la documentación técnica."))
    s.append(p("Búsquedas booleanas que guardo como alertas", "h2"))
    for consulta in [
        '("desarrollador backend junior" OR "junior backend developer" OR "python developer junior") '
        'AND ("Django" OR "Python") NOT senior NOT lead',
        '("desarrollador web junior") AND ("Python" OR "Django" OR "SQL") NOT senior location:Chile',
        '("trainee developer" OR "desarrollador trainee") AND ("Python" OR "JavaScript") NOT senior NOT mid',
    ]:
        caja = Table([[Paragraph(consulta, E["code"])]], colWidths=[ancho])
        caja.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef2f9")),
            ("BOX", (0, 0), (-1, -1), 0.7, LINE),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        s.append(caja)
        s.append(Spacer(1, 6))
    s.append(p("Publicación #OpenToWork", "h2"))
    s.append(p(
        "Estoy en búsqueda de mi primera oportunidad como Desarrollador Junior en Python y Django. "
        "#OpenToWork. Durante mi formación construí tres productos completos: Alke Wallet (billetera "
        "digital en Django con 36 pruebas automatizadas), TaskMaster (gestión de proyectos con "
        "autenticación y dashboard) y ClickAndGo (e-commerce con SQLite y guion de pruebas). "
        "Busco un rol junior o trainee en desarrollo backend o web, remoto o híbrido en Chile. "
        "Portafolio: migueltroncoso.github.io/modulo_8"))

    s.append(p("7. Métricas y seguimiento", "h2"))
    s.append(caja_datos([("10", "Postulaciones/semana"), ("5", "Conexiones/semana"),
                         ("2", "Simulaciones/semana"), ("20%", "Tasa de respuesta")]))
    s.append(Spacer(1, 8))
    s.append(tabla(
        [[p("Empresa", "cellh"), p("Puesto", "cellh"), p("Canal", "cellh"), p("Estado", "cellh")],
         [p("Fintual", "cellb"), p("Backend Junior", "cell"), p("LinkedIn", "cell"), p("Postulado", "cell")],
         [p("Buk", "cellb"), p("Desarrollador Web Junior", "cell"), p("GetOnBoard", "cell"), p("Entrevista", "cell")],
         [p("Defontana", "cellb"), p("Trainee Programador", "cell"), p("Laborum", "cell"), p("En revisión", "cell")],
         [p("Startup GetOnBoard", "cellb"), p("Junior Python Developer", "cell"), p("GetOnBoard", "cell"), p("Prueba técnica", "cell")]],
        [130, 165, 95, ancho - 390],
    ))
    s.append(Spacer(1, 4))
    s.append(p("Estados posibles: postulado, en revisión, entrevista, prueba técnica, oferta y cerrado.", "small"))

    s.append(PageBreak())
    s.append(p("8. Plantillas de contacto", "h2"))
    s.append(p("Postulación espontánea", "cellb"))
    s.append(p(
        "Asunto: CV para Desarrollo | Postulación espontánea - Miguel Troncoso<br/><br/>"
        "Hola: mi nombre es Miguel Troncoso y soy desarrollador web junior con foco en Python y "
        "Django. Les escribo porque me gustaría formar parte de su equipo y aportar en desarrollo "
        "backend. En mi formación construí una billetera digital con 36 pruebas automatizadas, una "
        "plataforma de gestión de proyectos y un e-commerce con persistencia en SQLite. Pueden ver "
        "el detalle en mi portafolio: migueltroncoso.github.io/modulo_8. Adjunto mi CV y quedo "
        "atento a cualquier oportunidad. Saludos cordiales, Miguel Troncoso.", "body"))
    s.append(Spacer(1, 6))
    s.append(p("Mensaje a reclutador", "cellb"))
    s.append(p(
        "Hola [Nombre], vi que eres reclutador especializado en tecnología. Soy desarrollador web "
        "junior con experiencia en Python, Django y SQL, y estoy explorando nuevas oportunidades. "
        "Me encantaría conectar y quedar disponible por si surge un rol junior o trainee que se "
        "ajuste a mi perfil. Portafolio: migueltroncoso.github.io/modulo_8. ¿Podríamos conversar? "
        "Gracias.", "body"))
    s.append(Spacer(1, 6))
    s.append(p("Agradecimiento posterior a la entrevista", "cellb"))
    s.append(p(
        "Hola [Nombre]: gracias por el tiempo de hoy en la entrevista para el puesto de [Puesto]. "
        "Me quedó muy clara la forma de trabajo del equipo y sigo muy interesado en la oportunidad. "
        "Quedo disponible por si necesitan algún antecedente adicional. Saludos cordiales, "
        "Miguel Troncoso.", "body"))

    s.append(p("9. Checklist de la búsqueda", "h2"))
    for item in [
        "CV de una página, revisado y en formato PDF con mi nombre en el archivo.",
        "Portafolio publicado y enlazado desde el CV y desde LinkedIn.",
        "Perfil de LinkedIn con titular, resumen, aptitudes y URL personalizada.",
        "Alertas de empleo configuradas con las búsquedas booleanas.",
        "Carta de presentación y correo de postulación listos para adaptar.",
        "Tracker de postulaciones actualizado cada semana.",
        "Rutina de horas de búsqueda sostenida de lunes a viernes.",
        "Preparación de entrevistas: pitch, banco STAR y preguntas al entrevistador.",
    ]:
        s.append(vineta(item))

    doc.build(s, onFirstPage=encabezado_pie(TITULO_PLAN), onLaterPages=encabezado_pie(TITULO_PLAN))
    return ruta


# --------------------------------------------------------------------------
# Documento 2: Guía de entrevistas y banco STAR
# --------------------------------------------------------------------------
def construir_entrevistas():
    ruta = os.path.join(DOCS, "Guia_Entrevistas_Miguel_Troncoso.pdf")
    doc = SimpleDocTemplate(ruta, pagesize=A4, leftMargin=48, rightMargin=48,
                            topMargin=52, bottomMargin=58,
                            title="Guia de Entrevistas y Banco STAR - Miguel Troncoso",
                            author="Miguel Troncoso")
    ancho = A4[0] - 96
    s = bloque_titulo(
        TITULO_ENTREVISTAS,
        "Preparación para entrevistas laborales en la industria TI: tipos de entrevista, checklist "
        "previo, comunicación efectiva, elevator pitch, banco de respuestas STAR y manejo de las "
        "emociones durante el proceso de búsqueda.",
    )

    s.append(p("1. Tipos de entrevista y cómo me preparo", "h2"))
    s.append(tabla(
        [[p("Tipo", "cellh"), p("Cómo me preparo", "cellh")],
         [p("Individual", "cellb"), p("Pitch, CV y ejemplos técnicos listos para explicar.", "cell")],
         [p("Grupal", "cellb"), p("Escuchar, aportar sin monopolizar y ordenar las ideas antes de hablar.", "cell")],
         [p("Dirigida", "cellb"), p("Respuestas concretas y estructuradas, sin divagar.", "cell")],
         [p("Libre", "cellb"), p("Guion propio para mantener el foco y no perder el hilo.", "cell")],
         [p("Mixta", "cellb"), p("Combinar claridad, ejemplos y métricas de mis proyectos.", "cell")],
         [p("Técnica / desafío", "cellb"), p("Explicar el razonamiento en voz alta mientras resuelvo.", "cell")],
         [p("Psicolaboral", "cellb"), p("Ser genuino y concentrarme en cumplir las consignas.", "cell")]],
        [140, ancho - 140],
    ))

    s.append(p("2. Preparación previa", "h2"))
    for item in [
        "<b>Empresa:</b> historia, misión, valores, productos, competidores y publicaciones recientes.",
        "<b>Puesto:</b> releer el aviso y mapear cada requisito con una evidencia propia.",
        "<b>CV:</b> repasarlo para hablar de su contenido sin leerlo.",
        "<b>Documentación:</b> CV actualizado, portafolio y ejemplos de código disponibles.",
        "<b>Preguntas:</b> preparar al menos tres para el entrevistador.",
        "<b>Pretensión salarial:</b> investigar un rango según el rol y mi experiencia.",
        "<b>Logística:</b> probar cámara, micrófono y conexión 15 minutos antes, o calcular la ruta con anticipación.",
        "<b>Vestimenta:</b> business casual, colores neutros, prolijidad e higiene personal.",
    ]:
        s.append(vineta(item))

    s.append(p("3. Durante la entrevista", "h2"))
    s.append(tabla(
        [[p("Elemento", "cellh"), p("Qué hago", "cellh")],
         [p("Comunicación verbal", "cellb"), p("Tono moderado, ideas ordenadas y respuestas concretas.", "cell")],
         [p("Comunicación no verbal", "cellb"), p("Postura firme, cuerpo orientado al entrevistador y gestos naturales.", "cell")],
         [p("Contacto visual", "cellb"), p("Mirada sostenida y natural, sin fijarla de forma incómoda.", "cell")],
         [p("Escucha activa", "cellb"), p("Escuchar completa la pregunta antes de responder.", "cell")],
         [p("Brecha comunicacional", "cellb"), p("Verificar que el mensaje se entendió y reformular si es necesario.", "cell")],
         [p("Cierre", "cellb"), p("Agradecer, reafirmar el interés y preguntar los próximos pasos.", "cell")]],
        [150, ancho - 150],
    ))

    s.append(PageBreak())
    s.append(p("4. Elevator pitch", "h2"))
    s.append(p(
        "Presentación breve de 30 a 60 segundos con la estructura: introducción, problema, solución "
        "y valor diferencial."))
    s.append(p("Versión de 30 segundos", "cellb"))
    s.append(p(
        "Hola, soy Miguel Troncoso, desarrollador web junior especializado en Python y Django. "
        "Construí una billetera digital con 36 pruebas automatizadas, una plataforma de gestión de "
        "proyectos y un e-commerce con SQLite. Me enfoco en el backend y en la integridad de los "
        "datos. Busco mi primera oportunidad junior para seguir creciendo y aportar a un equipo "
        "de producto.", "body"))
    s.append(p("Versión de 60 segundos", "cellb"))
    s.append(p(
        "Hola, soy Miguel Troncoso. Vengo de una formación intensiva en desarrollo de software y me "
        "especialicé en backend con Python y Django. En los últimos proyectos trabajé un problema "
        "que aparece en cualquier producto con datos: mantener la información íntegra. En Alke "
        "Wallet implementé transacciones atómicas para que los saldos nunca quedaran inconsistentes "
        "y lo respaldé con 36 pruebas automatizadas. También construí TaskMaster, una plataforma de "
        "gestión de proyectos con autenticación y dashboard, y ClickAndGo, un e-commerce con "
        "persistencia en SQLite y guion de pruebas. Lo que aporto es un perfil junior que ya trabajó "
        "el ciclo completo: modelo de datos, lógica de negocio, interfaz y pruebas. Busco un rol "
        "junior o trainee en backend o desarrollo web, remoto o híbrido en Chile.", "body"))

    s.append(p("5. Banco de respuestas STAR", "h2"))
    s.append(p(
        "La metodología STAR estructura las respuestas en Situación, Tarea, Acción y Resultado. "
        "Estas respuestas usan evidencia real de mis proyectos.", "body"))

    preguntas = [
        (
            "Cuéntame sobre un desafío técnico que hayas enfrentado",
            [
                ("Situación", "En Alke Wallet, una billetera digital en Django, los saldos debían mantenerse correctos aunque se registraran retiros, transferencias y operaciones simultáneas."),
                ("Tarea", "Impedir saldos negativos y transferencias inválidas sin romper la experiencia del usuario ni la integridad de la base de datos."),
                ("Acción", "Implementé la actualización de saldo dentro de una transacción atómica con select_for_update, validaciones de negocio en el modelo y reversa automática al eliminar un movimiento."),
                ("Resultado", "36 pruebas automatizadas aprobadas, cobertura completa del CRUD y cero regresiones de saldo detectadas en la suite."),
            ],
        ),
        (
            "Háblame de un proyecto del que estés orgulloso",
            [
                ("Situación", "Necesitaba un proyecto que demostrara dominio del ORM y no solo formularios básicos."),
                ("Tarea", "Construir una aplicación con relaciones 1:1, 1:N y M:N, migraciones, consultas personalizadas y pruebas."),
                ("Acción", "Desarrollé Alke Wallet con cinco modelos, seis consultas avanzadas (incluido SQL con raw() y cursores) y una suite de 36 pruebas."),
                ("Resultado", "Es el caso de estudio de mi portafolio y el proyecto que mejor explica mi forma de trabajar con datos."),
            ],
        ),
        (
            "¿Cómo manejas los errores y el feedback?",
            [
                ("Situación", "Durante el desarrollo recibí observaciones sobre nombres de variables, orden del código y validaciones faltantes."),
                ("Tarea", "Corregir sin romper funcionalidades ya probadas y sin repetir el mismo error."),
                ("Acción", "Antes de cada cambio revisaba la suite de pruebas, corregía, volvía a ejecutar los tests y aplicaba el criterio en los siguientes módulos."),
                ("Resultado", "Las correcciones quedaron cubiertas por pruebas y el código final es más legible y consistente."),
            ],
        ),
        (
            "¿Cómo priorizas cuando tienes varias tareas a la vez?",
            [
                ("Situación", "En ClickAndGo había que avanzar en varias capas a la vez: modelo, DAO, servicios y pruebas."),
                ("Tarea", "Entregar un sistema funcional sin dejar funcionalidades a medias."),
                ("Acción", "Trabajé por bloques con checklists, prioricé primero lo que bloqueaba al resto (modelo y DAO) y validé cada avance con el guion de pruebas P01-P19."),
                ("Resultado", "El sistema quedó completo, probado y con un guion de pruebas reproducible."),
            ],
        ),
        (
            "¿Cuál es tu mayor debilidad?",
            [
                ("Situación", "Mi experiencia es junior y todavía no he trabajado en un equipo con procesos formales de producción."),
                ("Tarea", "Reducir esa brecha antes y durante mi primer empleo."),
                ("Acción", "Estoy aprendiendo Django REST Framework para construir APIs y tengo planificado sumar Docker y despliegue en la nube."),
                ("Resultado", "Ya pasé de solo CRUD a razonar sobre integridad y pruebas. El siguiente paso es hacerlo en un entorno de equipo."),
            ],
        ),
        (
            "¿Dónde te ves en cinco años?",
            [
                ("Situación", "Hoy soy junior y quiero construir una carrera en backend."),
                ("Tarea", "Definir un camino de crecimiento realista."),
                ("Acción", "Mi plan es profundizar en Python, APIs y bases de datos, y ganar experiencia en producto y despliegue."),
                ("Resultado", "En cinco años espero ser un desarrollador backend consolidado, capaz de liderar una funcionalidad completa y mentorizar a alguien que recién empieza."),
            ],
        ),
    ]

    for titulo, filas in preguntas:
        bloque = [p(titulo, "cellb"), Spacer(1, 3)]
        filas_tabla = []
        for etiqueta, texto in filas:
            filas_tabla.append([p(etiqueta, "cellb"), p(texto, "cell")])
        bloque.append(tabla(filas_tabla, [72, ancho - 72], encabezado=False))
        bloque.append(Spacer(1, 10))
        s.append(KeepTogether(bloque))

    s.append(PageBreak())
    s.append(p("6. Preguntas para el entrevistador", "h2"))
    for item in [
        "¿Cómo se organizan los equipos de producto y cuánto ownership tiene un perfil junior sobre el ciclo completo?",
        "¿Qué estrategia de testing y control de calidad utilizan en sus productos?",
        "¿Cómo es el proceso de onboarding y mentoría para perfiles junior y qué se espera en los primeros tres meses?",
        "¿Cuáles consideran que son los principales desafíos de este rol?",
        "¿Cómo continúa el proceso y en qué fecha estiman contactar a las personas seleccionadas?",
    ]:
        s.append(vineta(item))

    s.append(p("7. Manejo emocional de la búsqueda", "h2"))
    s.append(tabla(
        [[p("Aspecto", "cellh"), p("Cómo lo aplico", "cellh")],
         [p("Autoconciencia", "cellb"), p("Registro cómo me siento después de cada entrevista y proceso.", "cell")],
         [p("Autorregulación", "cellb"), p("No respondo ni postulo desde la frustración.", "cell")],
         [p("Motivación", "cellb"), p("Celebro avances pequeños, como una entrevista agendada.", "cell")],
         [p("Empatía", "cellb"), p("Entiendo que el reclutador también tiene tiempos y procesos internos.", "cell")],
         [p("Habilidad social", "cellb"), p("Mantengo mi red activa más allá de las postulaciones.", "cell")]],
        [150, ancho - 150],
    ))

    s.append(p("8. Checklist final", "h2"))
    for item in [
        "<b>Antes:</b> investigar, repasar el CV, preparar el pitch, definir salario y probar los equipos.",
        "<b>Durante:</b> puntualidad, escucha activa, respuestas STAR, contacto visual y preguntas al entrevistador.",
        "<b>Después:</b> correo de agradecimiento, registro en el tracker y autoevaluación de la entrevista.",
    ]:
        s.append(vineta(item))
    s.append(Spacer(1, 8))
    s.append(p(
        "La práctica constante es lo que da seguridad. Ensayar el pitch y las respuestas STAR en voz "
        "alta, con cronómetro y frente a otra persona, es la mejor preparación para una entrevista "
        "real.", "body"))

    doc.build(s, onFirstPage=encabezado_pie(TITULO_ENTREVISTAS),
              onLaterPages=encabezado_pie(TITULO_ENTREVISTAS))
    return ruta


if __name__ == "__main__":
    os.makedirs(DOCS, exist_ok=True)
    print("Generado:", construir_plan())
    print("Generado:", construir_entrevistas())
