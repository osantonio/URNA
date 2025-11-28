/**
 * Utilidades para renderizar nombres cortos
 */

/**
 * Renderiza nombres cortos (primer nombre + primer apellido)
 */
export function renderShortNames() {
    const nameCells = Array.from(document.querySelectorAll('#votantes-body .font-medium.text-foreground'));
    nameCells.forEach(el => {
        const nombres = (el.getAttribute('data-nombres') || '').trim();
        const apellidos = (el.getAttribute('data-apellidos') || '').trim();
        const full = (el.getAttribute('data-fullname') || '').trim();
        const firstName = nombres ? nombres.split(/\s+/)[0] : '';
        const firstLast = apellidos ? apellidos.split(/\s+/)[0] : '';
        el.textContent = `${firstName} ${firstLast}`.trim();
        const hidden = document.createElement('span');
        hidden.className = 'hidden';
        hidden.textContent = full;
        el.appendChild(hidden);
    });
}

/**
 * Renderiza nombres cortos de referentes
 */
export function renderShortRefNames() {
    const refCells = Array.from(document.querySelectorAll('#votantes-body .ref-name'));
    refCells.forEach(el => {
        const nombres = (el.getAttribute('data-ref-nombres') || '').trim();
        const apellidos = (el.getAttribute('data-ref-apellidos') || '').trim();
        const full = (el.getAttribute('data-ref-fullname') || '').trim();
        const firstName = nombres ? nombres.split(/\s+/)[0] : '';
        const firstLast = apellidos ? apellidos.split(/\s+/)[0] : '';
        el.textContent = `${firstName} ${firstLast}`.trim();
        const hidden = document.createElement('span');
        hidden.className = 'hidden';
        hidden.textContent = full;
        el.appendChild(hidden);
    });
}
