/**
 * Módulo de filtrado y búsqueda de votantes
 */

import { normalize } from './utils.js';

// Mapeo de claves de búsqueda a campos de datos
const keyMap = {
    'nombre': 'name', 'nombres': 'name', 'apellidos': 'name', 'votante': 'name',
    'identificacion': 'id', 'id': 'id', 'cc': 'id',
    'telefono': 'phone',
    'puesto': 'place', 'lugar': 'place', 'lugar_votacion': 'place',
    'mesa': 'table', 'mesa_votacion': 'table',
    'rol': 'role',
    'referido': 'ref', 'asignado_a': 'ref', 'referente': 'ref',
    'sexo': 'sex', 'genero': 'sex',
};

/**
 * Parsea el valor de entrada y extrae filtros y tokens
 */
export function parseFilters(value) {
    const raw = (value || '').trim();
    const result = { filters: [], tokens: [], error: null };
    if (!raw) return result;

    const cleaned = raw.replace(/[()]/g, '');
    const parts = cleaned.split(',').map(p => p.trim()).filter(Boolean);

    for (const part of parts) {
        const idx = part.indexOf(':');
        if (idx !== -1) {
            const key = normalize(part.slice(0, idx));
            const val = part.slice(idx + 1).trim();
            if (!val) {
                result.error = 'Sintaxis inválida: valor vacío';
                continue;
            }
            result.filters.push({ key, value: val });
        } else {
            result.tokens.push(part);
        }
    }
    return result;
}

/**
 * Extrae datos de una fila para filtrado
 */
export function getRowData(row) {
    const nameEl = row.querySelector('.font-medium.text-foreground');
    const idEl = row.querySelector('.id-badge');
    const phoneEl = row.children[1]?.querySelector('span, a');
    const placeEl = row.children[2]?.querySelector('span');
    const tableEl = row.children[3]?.querySelector('span');
    const roleEl = row.children[4]?.querySelector('span');
    const refEl = row.children[5]?.querySelector('.ref-name, span');
    const sexo = row.getAttribute('data-sexo') || '';

    return {
        name: normalize(nameEl?.getAttribute('data-fullname') || nameEl?.textContent || ''),
        id: normalize(idEl?.getAttribute('data-id') || ''),
        phone: normalize(phoneEl?.textContent || ''),
        place: normalize(placeEl?.textContent || ''),
        table: normalize(tableEl?.textContent || ''),
        role: normalize(roleEl?.textContent || ''),
        ref: normalize(refEl?.textContent || ''),
        sex: normalize(sexo),
        text: normalize(row.textContent || ''),
    };
}

/**
 * Renderiza badges de filtros activos
 */
export function renderBadges(parsed, badgesEl) {
    badgesEl.innerHTML = '';
    if (parsed.filters.length === 0 && parsed.tokens.length === 0) return;

    const frag = document.createDocumentFragment();
    parsed.filters.forEach(f => {
        const b = document.createElement('span');
        b.className = 'filter-badge';
        b.textContent = `${f.key}: ${f.value}`;
        frag.appendChild(b);
    });
    parsed.tokens.forEach(t => {
        const b = document.createElement('span');
        b.className = 'filter-badge';
        b.textContent = t;
        frag.appendChild(b);
    });
    badgesEl.appendChild(frag);
}

/**
 * Aplica filtros a las filas
 */
export function applyFilters(parsed, rows, keyMap) {
    let visible = 0;

    if (!parsed.filters.length && !parsed.tokens.length) {
        rows.forEach(r => r.classList.remove('hidden'));
        return rows.length;
    }

    rows.forEach(r => {
        const data = getRowData(r);
        let match = true;

        for (const f of parsed.filters) {
            const k = keyMap[f.key] || f.key;
            const val = normalize(f.value);
            if (!data[k] || data[k].indexOf(val) === -1) {
                match = false;
                break;
            }
        }

        if (match && parsed.tokens.length) {
            for (const t of parsed.tokens) {
                const token = normalize(t);
                if (data.text.indexOf(token) === -1) {
                    match = false;
                    break;
                }
            }
        }

        if (match) {
            r.classList.remove('hidden');
            visible += 1;
        } else {
            r.classList.add('hidden');
        }
    });

    return visible;
}

export { keyMap };
