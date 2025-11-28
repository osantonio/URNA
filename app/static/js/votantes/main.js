/**
 * Módulo principal para gestión de listado de votantes
 */

import { parseFilters, renderBadges, applyFilters, keyMap } from './filters.js';
import { Pagination } from './pagination.js';
import { renderShortNames, renderShortRefNames } from './nameUtils.js';
import { wireCopyIds } from './idBadge.js';

// Elementos del DOM
const input = document.getElementById('search-input');
const tbody = document.getElementById('votantes-body');
const rows = Array.from(tbody.querySelectorAll('tr')).filter(r => r.id !== 'no-results');
const noResults = document.getElementById('no-results');
const countEl = document.getElementById('search-count');
const badgesEl = document.getElementById('filter-badges');
const errorEl = document.getElementById('filter-error');
const paginationEl = document.getElementById('pagination');

// Inicializar paginación
const pagination = new Pagination(paginationEl);

// Timer para debounce
let timer = null;

/**
 * Aplica filtros y actualiza la vista
 */
function applyFilter(skipResetPage) {
    const parsed = parseFilters(input.value);
    errorEl.textContent = parsed.error || '';
    renderBadges(parsed, badgesEl);

    const visible = applyFilters(parsed, rows, keyMap);

    if (noResults) {
        if (visible === 0) noResults.classList.remove('hidden');
        else noResults.classList.add('hidden');
    }

    if (!skipResetPage) pagination.reset();
    pagination.render(visible);
    pagination.applyPagination(rows);

    if (countEl) {
        countEl.textContent = visible ? `${visible} resultado(s)` : '0 resultados';
    }
}

/**
 * Filtro con debounce
 */
function debouncedFilter() {
    if (timer) clearTimeout(timer);
    timer = setTimeout(applyFilter, 200);
}

// Configurar callback de paginación
pagination.onPageChange = applyFilter;

// Inicialización
renderShortNames();
renderShortRefNames();
wireCopyIds();

if (input) {
    input.addEventListener('input', debouncedFilter);
    applyFilter();
}
