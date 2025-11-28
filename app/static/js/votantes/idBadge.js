/**
 * Funcionalidad para copiar ID al portapapeles
 */

export function wireCopyIds() {
    const badges = Array.from(document.querySelectorAll('.id-badge'));
    badges.forEach(badge => {
        const tooltip = badge.parentElement.querySelector('.copy-tooltip');
        const copyNumber = () => {
            const id = badge.getAttribute('data-id') || '';
            if (!id) return;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(id).then(() => {
                    if (tooltip) {
                        tooltip.classList.add('visible');
                        setTimeout(() => tooltip.classList.remove('visible'), 1200);
                    }
                }).catch(() => { });
            }
        };
        badge.addEventListener('click', copyNumber);
        badge.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                copyNumber();
            }
        });
    });
}
