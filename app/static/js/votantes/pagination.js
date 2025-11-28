/**
 * Módulo de paginación
 */

const PAGE_SIZE = 25;

export class Pagination {
    constructor(paginationEl) {
        this.paginationEl = paginationEl;
        this.currentPage = 1;
        this.onPageChange = null;
    }

    render(total) {
        this.paginationEl.innerHTML = '';
        const pages = Math.ceil(total / PAGE_SIZE) || 1;
        if (pages <= 1) return;

        const prev = document.createElement('button');
        prev.className = 'page-btn';
        prev.textContent = 'Anterior';
        prev.disabled = this.currentPage === 1;
        prev.addEventListener('click', () => {
            this.currentPage = Math.max(1, this.currentPage - 1);
            if (this.onPageChange) this.onPageChange(true);
        });

        const next = document.createElement('button');
        next.className = 'page-btn';
        next.textContent = 'Siguiente';
        next.disabled = this.currentPage === pages;
        next.addEventListener('click', () => {
            this.currentPage = Math.min(pages, this.currentPage + 1);
            if (this.onPageChange) this.onPageChange(true);
        });

        const info = document.createElement('span');
        info.className = 'page-info';
        info.textContent = `Página ${this.currentPage} de ${pages}`;

        this.paginationEl.appendChild(prev);
        this.paginationEl.appendChild(info);
        this.paginationEl.appendChild(next);
    }

    applyPagination(rows) {
        const start = (this.currentPage - 1) * PAGE_SIZE;
        const end = start + PAGE_SIZE;
        let idx = 0;

        rows.forEach(r => {
            if (r.classList.contains('hidden')) return;
            const shouldHide = idx < start || idx >= end;
            r.classList.toggle('hidden-page', shouldHide);
            idx += 1;
        });
    }

    reset() {
        this.currentPage = 1;
    }
}
