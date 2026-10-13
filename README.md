# 💼 Kit de Empleabilidad Digital — Miguel Troncoso

### Evaluación Módulo 9: Desarrollo de empleabilidad en la industria digital

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-121013?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

---

## 🔗 Kit en línea

**<https://migueltroncoso.github.io/modulo_9/>**

Sitio estático publicado con **GitHub Pages**. Reúne el perfil profesional, el plan de búsqueda
laboral, el CV, la estrategia de LinkedIn, la preparación de entrevistas, el banco de respuestas STAR
y las plantillas de contacto.

### Documentos de entrega

| Documento | Enlace |
| :--- | :--- |
| 📋 Plan de búsqueda laboral | [`docs/Plan_Busqueda_Laboral_Miguel_Troncoso.pdf`](docs/Plan_Busqueda_Laboral_Miguel_Troncoso.pdf) |
| 🎤 Guía de entrevistas y banco STAR | [`docs/Guia_Entrevistas_Miguel_Troncoso.pdf`](docs/Guia_Entrevistas_Miguel_Troncoso.pdf) |
| 📄 Currículum Vitae | [`docs/CV_Miguel_Troncoso.pdf`](docs/CV_Miguel_Troncoso.pdf) |
| 📝 Informe del módulo | [`docs/Entrega_Modulo_9_Miguel_Troncoso.md`](docs/Entrega_Modulo_9_Miguel_Troncoso.md) |

---

## 📌 Descripción

Este repositorio contiene las herramientas de empleabilidad desarrolladas para la evaluación del
Módulo 9. El objetivo es preparar de forma estratégica la búsqueda de una primera oportunidad
profesional en la industria TI: saber qué buscar, cómo presentarse, dónde publicar el perfil y cómo
enfrentar cada etapa de un proceso de selección.

El kit se construyó como un **producto digital propio** (sitio web responsive con HTML, CSS y
JavaScript) y se complementa con documentos PDF listos para usar.

---

## 📋 Matriz de cumplimiento de la consigna

| Requerimiento | Entregable | Estado |
| :--- | :--- | :---: |
| **Plan de búsqueda laboral (AE1)** | Objetivo, dedicación semanal, puestos objetivo, empresas, canales y métricas. | ✅ |
| **Perfil profesional y seniority** | Sección *Perfil* con rol objetivo, competencias técnicas, blandas y propuesta de valor. | ✅ |
| **Confección del CV (AE2)** | CV de una página, optimizado para ATS y enlazado al portafolio. | ✅ |
| **Publicación y difusión del CV (AE2)** | Estrategia para LinkedIn, portales laborales y postulación espontánea. | ✅ |
| **Perfil de LinkedIn optimizado** | Titular, resumen, aptitudes, URL personalizada, búsquedas booleanas y post #OpenToWork. | ✅ |
| **Entrevistas laborales (AE3)** | Tipos de entrevista, checklist antes/durante/después y comunicación efectiva. | ✅ |
| **Metodología STAR** | Banco de 7 respuestas STAR construidas con evidencia real de los proyectos. | ✅ |
| **Elevator pitch** | Estructura y guiones de 30 y 60 segundos, listos para copiar y practicar. | ✅ |
| **Inteligencia emocional** | Estrategias de manejo emocional durante la búsqueda laboral. | ✅ |
| **Seguimiento** | Tracker de postulaciones con estados y próximos pasos. | ✅ |

---

## 🧭 Contenido del sitio

| Sección | Contenido |
| :--- | :--- |
| **Inicio** | Presentación, elevator pitch de 30 segundos y accesos a los documentos. |
| **Perfil** | Resumen profesional, competencias técnicas y blandas, propuesta de valor. |
| **Plan** | Objetivo SMART, dedicación semanal, puestos, empresas, canales y métricas. |
| **CV** | Secciones incluidas, reglas aplicadas y descarga del PDF. |
| **LinkedIn** | Titular, resumen, búsquedas booleanas y post #OpenToWork para copiar. |
| **Entrevistas** | Checklists antes, durante y después, tipos de entrevista y manejo emocional. |
| **Banco STAR** | Siete preguntas frecuentes con respuestas estructuradas. |
| **Pitch** | Estructura del pitch y versiones de 30 y 60 segundos. |
| **Tracker** | Tabla de seguimiento de postulaciones con estados. |
| **Plantillas** | Correo de postulación espontánea, mensaje a reclutador y agradecimiento. |
| **Contacto** | Email, GitHub, LinkedIn y disponibilidad. |

---

## 🗂️ Estructura del repositorio

```
modulo_9/
├── index.html                        # Sitio del kit de empleabilidad
├── .nojekyll                         # Evita el procesamiento Jekyll en GitHub Pages
├── assets/
│   ├── css/styles.css                # Tema oscuro y diseño responsive
│   ├── js/main.js                    # Navegación, animaciones y copiar al portapapeles
│   └── img/                          # Avatar, favicon e imágenes de proyectos
├── docs/
│   ├── Plan_Busqueda_Laboral_Miguel_Troncoso.pdf
│   ├── Guia_Entrevistas_Miguel_Troncoso.pdf
│   ├── CV_Miguel_Troncoso.pdf
│   ├── Entrega_Modulo_9_Miguel_Troncoso.md
│   └── screenshots/                  # Capturas del sitio
├── tools/
│   ├── build_docs.py                 # Genera el plan y la guía de entrevistas
│   ├── build_cv_pdf.py               # Genera el CV en PDF
│   └── capture_site.py               # Genera las capturas con Playwright
└── README.md
```

---

## ▶️ Ejecución local

```bash
git clone https://github.com/MiguelTroncoso/modulo_9.git
cd modulo_9
python3 -m http.server 8000
# Abrir http://127.0.0.1:8000
```

### Regenerar los documentos (opcional)

```bash
# Plan de búsqueda y guía de entrevistas (requiere reportlab)
python3 tools/build_docs.py

# CV en PDF
python3 tools/build_cv_pdf.py

# Capturas del sitio (requiere playwright + Chrome)
python3 tools/capture_site.py
```

---

## ✅ Calidad

- **Funcionalidad:** navegación, botones de copiado y descargas verificados.
- **Usabilidad:** diseño responsive, menú móvil, foco visible y `skip-link` accesible.
- **Rendimiento:** sitio sin dependencias de build y con imágenes optimizadas.
- **SEO:** `title`, `description`, Open Graph, favicon y `lang="es"`.
- **Accesibilidad:** contraste alto, etiquetas ARIA y navegación por teclado.

---

## 👨‍💻 Autor

- **Miguel Troncoso**
- Email: [miguel.troncoso36@gmail.com](mailto:miguel.troncoso36@gmail.com)
- GitHub: [@MiguelTroncoso](https://github.com/MiguelTroncoso)
- LinkedIn: [linkedin.com/in/miguel-troncoso](https://www.linkedin.com/in/miguel-troncoso/)
- Portafolio técnico: <https://migueltroncoso.github.io/modulo_8/>
- Kit de empleabilidad: <https://migueltroncoso.github.io/modulo_9/>
- Evaluación: **Módulo 9 — Desarrollo de empleabilidad en la industria digital**
