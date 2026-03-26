// ===== TEMA ESCURO =====
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    const themeIcon = themeToggle.querySelector('.theme-icon');

    // Apenas atualizar o ícone baseado no tema já aplicado
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    themeIcon.textContent = currentTheme === 'dark' ? '🌙' : '☀️';

    // Configurar botão para alternar
    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        themeIcon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    });
});

// ===== TOAST NOTIFICATION =====
function showToast(message, type = 'success', duration = 3000) {
    const toast = document.getElementById('toast');
    if (!toast) return;

    const toastIcon = document.getElementById('toast-icon');
    const toastMessage = document.getElementById('toast-message');

    const icons = {
        success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️'
    };

    toast.classList.remove('success', 'error', 'warning', 'info');
    toast.classList.add(type);
    toastIcon.textContent = icons[type] || '✅';
    toastMessage.textContent = message;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, duration);
}

// ===== MODAL PERSONALIZADO =====
const ConfirmModal = {
    modal: document.getElementById('confirmModal'),
    title: document.getElementById('modalTitle'),
    message: document.getElementById('modalMessage'),
    detail: document.getElementById('modalDetail'),
    cancelBtn: document.getElementById('modalCancel'),
    confirmBtn: document.getElementById('modalConfirm'),
    closeBtn: document.getElementById('modalClose'),
    resolvePromise: null,

    init() {
        if (!this.modal) return;

        this.cancelBtn?.addEventListener('click', () => this.close(false));
        this.confirmBtn?.addEventListener('click', () => this.close(true));
        this.closeBtn?.addEventListener('click', () => this.close(false));

        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close(false);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'flex') {
                this.close(false);
            }
        });
    },

    open(options = {}) {
        const { title = 'Confirmar exclusão', message = '', detail = '' } = options;

        this.title.textContent = title;
        this.message.textContent = message;
        this.detail.textContent = detail;
        this.detail.style.display = detail ? 'block' : 'none';

        this.modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        return new Promise((resolve) => {
            this.resolvePromise = resolve;
        });
    },

    close(result) {
        this.modal.style.display = 'none';
        document.body.style.overflow = '';
        if (this.resolvePromise) {
            this.resolvePromise(result);
            this.resolvePromise = null;
        }
    }
};

// Inicializar modal
document.addEventListener('DOMContentLoaded', () => ConfirmModal.init());

// Funções de confirmação
window.confirmarExclusao = async (nomeArquivo) => {
    return await ConfirmModal.open({
        title: 'Excluir arquivo',
        message: 'Tem certeza que deseja excluir este arquivo?',
        detail: nomeArquivo
    });
};

window.confirmarExclusaoPasta = async (nomePasta) => {
    return await ConfirmModal.open({
        title: '⚠️ Excluir pasta',
        message: 'ATENÇÃO! Todos os arquivos dentro dela serão apagados permanentemente.',
        detail: nomePasta
    });
};