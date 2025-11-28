/**
 * Utilidades para normalización y procesamiento de texto
 */

export function normalize(s) {
    return (s || '').toString().normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}
