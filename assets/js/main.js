/* ==========================================================================
   Kit de Empleabilidad Digital - Miguel Troncoso - Módulo 9
   Navegación, progreso de scroll, animaciones, copiar al portapapeles y toast.
   ========================================================================== */
(function () {
  "use strict";

  const header = document.getElementById("site-header");
  const progress = document.getElementById("scroll-progress");
  const navToggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("primary-nav");
  const toTop = document.getElementById("to-top");
  const toast = document.getElementById("toast");
  const navLinks = Array.from(document.querySelectorAll('.primary-nav a[href^="#"]'));
  const sections = Array.from(document.querySelectorAll("main section[id]"));

  /* ---------- Menú móvil ---------- */
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
      document.body.classList.toggle("nav-open", !open);
    });
    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        navToggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        document.body.classList.remove("nav-open");
      }
    });
  }

  /* ---------- Scroll ---------- */
  const onScroll = () => {
    const scrolled = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", scrolled > 8);
    if (progress) {
      const height = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (height > 0 ? (scrolled / height) * 100 : 0) + "%";
    }
    if (toTop) toTop.classList.toggle("is-visible", scrolled > 600);

    let current = "";
    for (const section of sections) {
      if (scrolled >= section.offsetTop - 150) current = section.id;
    }
    navLinks.forEach((link) => {
      const active = link.getAttribute("href") === "#" + current;
      link.classList.toggle("is-active", active && !link.classList.contains("nav-cta"));
    });
  };

  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          onScroll();
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );
  onScroll();

  if (toTop) toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  /* ---------- Animación de aparición ---------- */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el, index) => {
      el.style.transitionDelay = Math.min(index % 4, 3) * 70 + "ms";
      observer.observe(el);
    });
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Copiar al portapapeles ---------- */
  const mostrarToast = (mensaje) => {
    if (!toast) return;
    toast.textContent = mensaje;
    toast.classList.add("is-visible");
    window.clearTimeout(mostrarToast._t);
    mostrarToast._t = window.setTimeout(() => toast.classList.remove("is-visible"), 2200);
  };

  const copiarTexto = async (texto) => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(texto);
        return true;
      }
      const area = document.createElement("textarea");
      area.value = texto;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      const ok = document.execCommand("copy");
      document.body.removeChild(area);
      return ok;
    } catch (error) {
      return false;
    }
  };

  document.querySelectorAll("[data-copy]").forEach((boton) => {
    boton.addEventListener("click", async () => {
      const origen = document.querySelector(boton.getAttribute("data-copy"));
      if (!origen) return;
      const ok = await copiarTexto(origen.innerText.trim());
      mostrarToast(ok ? "Texto copiado al portapapeles" : "No se pudo copiar, selecciona el texto manualmente");
    });
  });

  /* ---------- Año dinámico ---------- */
  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
