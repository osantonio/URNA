// Dark mode toggle functionality - Flowbite style
const themeToggleBtn = document.getElementById('theme-toggle');
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');

// Función para sincronizar los iconos con el estado actual del tema
function syncIcons() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme === 'dark') {
        // En modo oscuro, mostrar el icono de sol (para cambiar a claro)
        themeToggleLightIcon.classList.remove('hidden');
        themeToggleDarkIcon.classList.add('hidden');
    } else {
        // En modo claro, mostrar el icono de luna (para cambiar a oscuro)
        themeToggleLightIcon.classList.add('hidden');
        themeToggleDarkIcon.classList.remove('hidden');
    }
}

// Inicializar si existen los elementos
if (themeToggleBtn && themeToggleLightIcon && themeToggleDarkIcon) {
    // Sincronizar iconos al cargar
    syncIcons();

    // Toggle dark mode al hacer click
    themeToggleBtn.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        let newTheme = 'light';

        if (currentTheme === 'light') {
            newTheme = 'dark';
        }

        // Aplicar nuevo tema
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('color-theme', newTheme);

        // Actualizar iconos
        syncIcons();
    });
}
