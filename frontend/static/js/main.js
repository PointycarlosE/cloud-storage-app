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

// Função para confirmar exclusão de arquivo
window.confirmarExclusao = async (nomeArquivo, form) => {
    console.log('confirmarExclusao chamado para:', nomeArquivo); // Debug
    
    const result = await ConfirmModal.open({
        title: 'Excluir arquivo',
        message: `Tem certeza que deseja excluir o arquivo "${nomeArquivo}"?`,
        detail: 'Esta ação não pode ser desfeita.'
    });
    
    console.log('Resultado da confirmação:', result); // Debug
    
    if (result) {
        // 🔥 SALVA INFO PARA MOSTRAR DEPOIS
        sessionStorage.setItem('toastMessage', `✅ "${nomeArquivo}" excluído com sucesso!`);
        sessionStorage.setItem('toastType', 'success');

        form.submit();
    }
    
    // Não retorna nada, pois já prevenimos o envio no HTML
};

// Função para confirmar exclusão de pasta
window.confirmarExclusaoPasta = async (nomePasta, form) => {
    console.log('confirmarExclusaoPasta chamado para:', nomePasta); // Debug
    
    const result = await ConfirmModal.open({
        title: '⚠️ Excluir pasta',
        message: `Tem certeza que deseja excluir a pasta "${nomePasta}"?`,
        detail: 'ATENÇÃO! TODOS os arquivos dentro dela serão apagados permanentemente.'
    });
    
    console.log('Resultado da confirmação:', result); // Debug
    
    if (result) {
        sessionStorage.setItem('toastMessage', `📁 "${nomePasta}" excluída com sucesso!`);
        sessionStorage.setItem('toastType', 'success');

        form.submit();
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const message = sessionStorage.getItem('toastMessage');
    const type = sessionStorage.getItem('toastType');

    if (message) {
        showToast(message, type || 'success');

        // limpar depois de usar
        sessionStorage.removeItem('toastMessage');
        sessionStorage.removeItem('toastType');
    }
});