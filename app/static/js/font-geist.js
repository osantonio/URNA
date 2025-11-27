// Activa la fuente Geist en todo el documento
// Añade la clase en el elemento raíz para aplicar las reglas CSS definidas en input.css
(() => {
  try {
    const cls = 'font-geist';
    const root = document.documentElement;
    if (!root.classList.contains(cls)) {
      root.classList.add(cls);
    }
  } catch (_) {
    // Fallback silencioso
  }
})();

