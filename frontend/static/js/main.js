// ===== CSRF TOKEN =====
// Lê o token CSRF do meta tag definido no explorar.html
// Usado em todas as requisições POST/AJAX para evitar ataques CSRF
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// ===== TEMA ESCURO =====
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    const themeIcon = themeToggle.querySelector('.theme-icon');
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    themeIcon.textContent = currentTheme === 'dark' ? '🌙' : '☀️';

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

    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

    toast.classList.remove('success', 'error', 'warning', 'info');
    toast.classList.add(type);
    toastIcon.textContent = icons[type] || '✅';
    toastMessage.textContent = message;
    toast.style.display = 'block';

    setTimeout(() => { toast.style.display = 'none'; }, duration);
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
        this.modal.addEventListener('click', (e) => { if (e.target === this.modal) this.close(false); });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'flex') this.close(false);
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
        return new Promise((resolve) => { this.resolvePromise = resolve; });
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

document.addEventListener('DOMContentLoaded', () => ConfirmModal.init());

// Confirmação de exclusão de arquivo (chamada pelo HTML inline)
window.confirmarExclusao = async (nomeArquivo, form) => {
    const result = await ConfirmModal.open({
        title: 'Excluir arquivo',
        message: `Tem certeza que deseja excluir o arquivo "${nomeArquivo}"?`,
        detail: 'Esta ação não pode ser desfeita.'
    });
    if (result) {
        sessionStorage.setItem('toastMessage', `✅ "${nomeArquivo}" excluído com sucesso!`);
        sessionStorage.setItem('toastType', 'success');
        form.submit();
    }
};

// Confirmação de exclusão de pasta (chamada pelo HTML inline)
window.confirmarExclusaoPasta = async (nomePasta, form) => {
    const result = await ConfirmModal.open({
        title: '⚠️ Excluir pasta',
        message: `Tem certeza que deseja excluir a pasta "${nomePasta}"?`,
        detail: 'ATENÇÃO! TODOS os arquivos dentro dela serão apagados permanentemente.'
    });
    if (result) {
        sessionStorage.setItem('toastMessage', `📁 "${nomePasta}" excluída com sucesso!`);
        sessionStorage.setItem('toastType', 'success');
        form.submit();
    }
};

// Exibir toast persistido no sessionStorage (após reload da página)
document.addEventListener('DOMContentLoaded', () => {
    const message = sessionStorage.getItem('toastMessage');
    const type = sessionStorage.getItem('toastType');
    if (message) {
        showToast(message, type || 'success');
        sessionStorage.removeItem('toastMessage');
        sessionStorage.removeItem('toastType');
    }
});

// ===== MOBILE MENU =====
document.addEventListener('DOMContentLoaded', function () {
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', function () { sidebar.classList.toggle('active'); });
        document.addEventListener('click', function (e) {
            if (window.innerWidth <= 768 && !sidebar.contains(e.target) && !mobileBtn.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
});

// ===== MODAL CRIAR PASTA =====
document.addEventListener('DOMContentLoaded', function () {
    const createFolderTrigger = document.getElementById('create-folder-trigger');
    const createFolderModal = document.getElementById('create-folder-modal');
    const closeFolderModal = document.getElementById('close-folder-modal');
    const cancelFolderModal = document.getElementById('cancel-folder-modal');

    const closeModal = () => { if (createFolderModal) createFolderModal.style.display = 'none'; };

    if (createFolderTrigger) {
        createFolderTrigger.addEventListener('click', function () {
            if (createFolderModal) createFolderModal.style.display = 'flex';
        });
    }

    if (closeFolderModal) closeFolderModal.addEventListener('click', closeModal);
    if (cancelFolderModal) cancelFolderModal.addEventListener('click', closeModal);
    if (createFolderModal) {
        createFolderModal.addEventListener('click', function (e) { if (e.target === createFolderModal) closeModal(); });
    }
});

// ===== UPLOAD DE ARQUIVOS =====
// Função central de upload — usada pelo botão, pelo drag & drop e pelo input file
window.uploadFiles = function (files) {
    if (!files || files.length === 0) return;

    const panel = document.getElementById('upload-panel');
    const list = document.getElementById('upload-list');

    if (panel) panel.style.display = 'flex';

    // Caminho atual extraído da URL (ex: /explorar/pasta/sub → /pasta/sub)
    const caminho = window.location.pathname.replace(/^\/explorar/, '') || '/';

    Array.from(files).forEach(file => {
        const item = document.createElement('div');
        item.className = 'upload-item';
        item.innerHTML = `
            <div class="upload-name">${escapeHtml(file.name)}</div>
            <div class="upload-bar"><div class="upload-fill"></div></div>
            <div class="upload-status">Enviando...</div>
        `;
        if (list) list.appendChild(item);

        const fill = item.querySelector('.upload-fill');
        const status = item.querySelector('.upload-status');

        const formData = new FormData();
        formData.append('arquivo', file);

        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/upload${caminho}`, true);

        // ✅ CSRF: obrigatório para o flask-wtf aceitar a requisição
        xhr.setRequestHeader('X-CSRFToken', getCsrfToken());

        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                if (fill) fill.style.width = percent + '%';
            }
        });

        xhr.onload = () => {
            if (xhr.status === 200 || xhr.status === 302) {
                if (fill) fill.style.width = '100%';
                if (status) status.textContent = 'Concluído ✓';
                item.classList.add('success');
                showToast(`✅ "${file.name}" enviado com sucesso!`, 'success');
                // Atualiza a listagem sem recarregar a página
                setTimeout(() => {
                    if (typeof atualizarLista === 'function') atualizarLista();
                }, 500);
            } else if (xhr.status === 400) {
                if (status) status.textContent = 'Tipo não permitido ✗';
                item.classList.add('error');
                showToast(`❌ Tipo de arquivo não permitido: "${file.name}"`, 'error');
            } else if (xhr.status === 413) {
                if (status) status.textContent = 'Arquivo muito grande ✗';
                item.classList.add('error');
                showToast(`❌ "${file.name}" excede o limite de tamanho`, 'error');
            } else {
                if (status) status.textContent = 'Erro ✗';
                item.classList.add('error');
                showToast(`❌ Erro ao enviar "${file.name}"`, 'error');
            }
        };

        xhr.onerror = () => {
            if (status) status.textContent = 'Erro de conexão';
            item.classList.add('error');
            showToast(`❌ Erro de conexão ao enviar "${file.name}"`, 'error');
        };

        xhr.send(formData);
    });
};

// ===== UPLOAD VIA BOTÃO (input file) =====
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        const uploadInput = document.getElementById('arquivo');
        const uploadBtn = document.querySelector('.upload-btn');

        if (uploadInput) {
            uploadInput.addEventListener('change', function (e) {
                const files = e.target.files;
                if (files && files.length > 0) {
                    window.uploadFiles(files);
                    uploadInput.value = ''; // Permite reselecionar os mesmos arquivos
                }
            });
        }

        if (uploadBtn && uploadInput) {
            // Substituir o nó para limpar listeners antigos
            const newBtn = uploadBtn.cloneNode(true);
            uploadBtn.parentNode.replaceChild(newBtn, uploadBtn);
            newBtn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                uploadInput.click();
            });
        }
    }, 100);
});

// ===== HELPER: ESCAPAR HTML =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}