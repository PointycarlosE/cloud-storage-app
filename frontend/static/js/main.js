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

// ===== MOBILE MENU =====
document.addEventListener('DOMContentLoaded', function () {
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    
    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });
        
        // Fechar sidebar ao clicar fora (mobile)
        document.addEventListener('click', function (e) {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && !mobileBtn.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
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
    const uploadInput = document.getElementById('arquivo');
    
    // Abrir modal criar pasta
    if (createFolderTrigger) {
        createFolderTrigger.addEventListener('click', function () {
            if (createFolderModal) {
                createFolderModal.style.display = 'flex';
            }
        });
    }
    
    // Fechar modal
    const closeModal = () => {
        if (createFolderModal) {
            createFolderModal.style.display = 'none';
        }
    };
    
    if (closeFolderModal) closeFolderModal.addEventListener('click', closeModal);
    if (cancelFolderModal) cancelFolderModal.addEventListener('click', closeModal);
    
    // Fechar ao clicar fora
    if (createFolderModal) {
        createFolderModal.addEventListener('click', function (e) {
            if (e.target === createFolderModal) {
                closeModal();
            }
        });
    }
    
    // Trigger upload file (mantendo funcionalidade)
    const uploadBtn = document.querySelector('.upload-btn');
    if (uploadBtn && uploadInput) {
        uploadBtn.addEventListener('click', function () {
            uploadInput.click();
        });
    }
    
    // Envio do formulário criar pasta via AJAX (opcional, para não recarregar)
    const folderForm = document.querySelector('#create-folder-modal form');
    if (folderForm) {
        folderForm.addEventListener('submit', function (e) {
            // Deixa o envio normal mesmo, já que recarrega a página
            // Mas fecha o modal
            closeModal();
        });
    }
});

// ===== UPLOAD AUTOMÁTICO (adicionar no final do main.js) =====
window.uploadFiles = function(files) {
    if (!files || files.length === 0) return;
    
    const panel = document.getElementById('upload-panel');
    const list = document.getElementById('upload-list');
    
    if (panel) panel.style.display = 'flex';
    
    const caminho = window.location.pathname.replace('/explorar', '');
    
    Array.from(files).forEach(file => {
        const item = document.createElement('div');
        item.className = 'upload-item';
        item.innerHTML = `
            <div class="upload-name">${escapeHtml(file.name)}</div>
            <div class="upload-bar">
                <div class="upload-fill"></div>
            </div>
            <div class="upload-status">Enviando...</div>
        `;
        
        if (list) list.appendChild(item);
        
        const fill = item.querySelector('.upload-fill');
        const status = item.querySelector('.upload-status');
        
        const formData = new FormData();
        formData.append('arquivo', file);
        
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/upload${caminho}`, true);
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                if (fill) fill.style.width = percent + '%';
            }
        });
        
        xhr.onload = () => {
            if (xhr.status === 200) {
                if (fill) fill.style.width = '100%';
                if (status) status.textContent = 'Concluído ✓';
                item.classList.add('success');
                showToast(`✅ "${file.name}" enviado com sucesso!`, 'success');
            } else {
                status.textContent = 'Erro ✗';
                item.classList.add('error');
                showToast(`❌ Erro ao enviar "${file.name}"`, 'error');
            }
        };
        
        xhr.onerror = () => {
            status.textContent = 'Erro de conexão';
            item.classList.add('error');
            showToast(`❌ Erro de conexão ao enviar "${file.name}"`, 'error');
        };
        
        xhr.send(formData);
    });
    
    // Atualizar a lista após os uploads
    setTimeout(() => {
        if (typeof atualizarLista === 'function') {
            atualizarLista();
        }
    }, 1000);
};

// Função auxiliar para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== UPLOAD VIA BOTÃO (selecionar arquivos) - VERSÃO ROBUSTA =====
document.addEventListener('DOMContentLoaded', function () {
    // Aguardar um pouco para garantir que o DOM está completamente carregado
    setTimeout(function() {
        const uploadInput = document.getElementById('arquivo');
        
        // Procurar o botão de upload de várias formas
        let uploadBtn = document.querySelector('.upload-btn');
        
        // Se não encontrar, tentar procurar por texto
        if (!uploadBtn) {
            const allButtons = document.querySelectorAll('.action-btn');
            allButtons.forEach(btn => {
                if (btn.textContent.includes('Upload') || btn.innerHTML.includes('📤')) {
                    uploadBtn = btn;
                }
            });
        }
        
        console.log('Upload button encontrado:', uploadBtn);
        console.log('Upload input encontrado:', uploadInput);
        
        if (uploadInput) {
            // Upload automático ao selecionar arquivos
            uploadInput.addEventListener('change', function (e) {
                const files = e.target.files;
                console.log('Arquivos selecionados:', files.length);
                if (files && files.length > 0) {
                    window.uploadFiles(files);
                    // Limpar o input para permitir selecionar os mesmos arquivos novamente
                    uploadInput.value = '';
                }
            });
        }
        
        // Trigger para abrir o seletor de arquivos ao clicar no botão
        if (uploadBtn && uploadInput) {
            // Remover event listeners antigos (se houver)
            const newBtn = uploadBtn.cloneNode(true);
            uploadBtn.parentNode.replaceChild(newBtn, uploadBtn);
            
            newBtn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Botão de upload clicado!');
                uploadInput.click();
            });
        } else {
            console.error('Botão ou input de upload não encontrado!');
        }
    }, 100);
});