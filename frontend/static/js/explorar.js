// Lightbox para imagens
document.addEventListener('DOMContentLoaded', function () {
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxInfo = document.getElementById('lightbox-info');
    const lightboxDownload = document.getElementById('lightbox-download');
    const lightboxDelete = document.getElementById('lightbox-delete');
    const lightboxClose = document.getElementById('lightbox-close');
    const lightboxPrev = document.getElementById('lightbox-prev');
    const lightboxNext = document.getElementById('lightbox-next');

    let currentImageIndex = 0;
    let images = [];

    function updateImageList() {
        images = [];
        document.querySelectorAll('.item-imagem').forEach((card, index) => {
            const link = card.closest('.item-link');
            if (link) {
                const thumbnail = card.querySelector('.item-thumbnail');
                const visualizarUrl = thumbnail ? thumbnail.src : '';
                const nomeElement = card.querySelector('.item-nome');
                const nome = nomeElement ? nomeElement.textContent : '';
                const downloadBtn = card.querySelector('.botao-download');
                const downloadUrl = downloadBtn ? downloadBtn.getAttribute('href') : '';
                const deleteForm = card.querySelector('form');

                images.push({
                    nome: nome,
                    visualizarUrl: visualizarUrl,
                    downloadUrl: downloadUrl,
                    deleteForm: deleteForm,
                    elemento: card,
                    index: index
                });
            }
        });
    }

    function openLightbox(index) {
        if (images.length === 0) return;

        currentImageIndex = index;
        const image = images[currentImageIndex];

        lightboxImage.src = image.visualizarUrl;
        lightboxTitle.textContent = image.nome;
        lightboxInfo.textContent = `Imagem ${currentImageIndex + 1} de ${images.length}`;
        lightboxDownload.href = image.downloadUrl;

        // Lightbox - botão de excluir
        lightboxDelete.onclick = async function (e) {
            e.preventDefault();
            const image = images[currentImageIndex];

            // Usar o modal personalizado
            const confirmado = await ConfirmModal.open({
                title: 'Excluir imagem',
                message: `Tem certeza que deseja excluir a imagem "${image.nome}"?`,
                detail: 'Esta ação não pode ser desfeita.'
            });

            if (confirmado) {
                if (image.deleteForm) {
                    showToast(`Excluindo ${image.nome}...`, 'info', 2000);

                    // Clonar o formulário e submeter
                    const form = image.deleteForm.cloneNode(true);
                    document.body.appendChild(form);

                    // Submeter o formulário clonado
                    form.submit();

                    // Remover o formulário após um pequeno delay
                    setTimeout(() => {
                        if (document.body.contains(form)) {
                            document.body.removeChild(form);
                        }
                    }, 1000);
                }
            }
        };

        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        lightboxImage.src = '';
        document.body.style.overflow = '';
    }

    function prevImage() {
        if (images.length > 0) {
            currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
            openLightbox(currentImageIndex);
        }
    }

    function nextImage() {
        if (images.length > 0) {
            currentImageIndex = (currentImageIndex + 1) % images.length;
            openLightbox(currentImageIndex);
        }
    }

    updateImageList();

    document.querySelectorAll('.item-imagem').forEach((card) => {
        const link = card.closest('.item-link');
        if (link) {
            link.addEventListener('click', function (e) {
                if (e.target.closest('.botao-download') ||
                    e.target.closest('.botao-excluir') ||
                    e.target.closest('form') ||
                    e.target.closest('button') ||
                    e.target.closest('.item-checkbox') ||
                    e.target.closest('.item-checkbox-input')) {
                    return;
                }

                e.preventDefault();
                e.stopPropagation();

                updateImageList();

                const currentCard = e.currentTarget.querySelector('.item-imagem');
                const newIndex = Array.from(document.querySelectorAll('.item-imagem')).indexOf(currentCard);

                if (newIndex !== -1) {
                    openLightbox(newIndex);
                }
            });
        }
    });

    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', prevImage);
    lightboxNext.addEventListener('click', nextImage);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }

        if (lightbox.classList.contains('active')) {
            if (e.key === 'ArrowLeft') {
                prevImage();
            } else if (e.key === 'ArrowRight') {
                nextImage();
            }
        }
    });

    lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
});

// ===== BARRA DE PESQUISA =====
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('pesquisa-input');
    const searchClear = document.getElementById('pesquisa-limpar');
    const searchCounter = document.getElementById('pesquisa-contador');
    const items = document.querySelectorAll('.item-link');
    let searchTimeout;

    function updateCounter(count) {
        if (count === 0) {
            searchCounter.textContent = 'Nenhum resultado';
        } else if (count === 1) {
            searchCounter.textContent = '1 resultado';
        } else {
            searchCounter.textContent = `${count} resultados`;
        }
    }

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();

        searchClear.classList.toggle('visible', searchTerm.length > 0);

        if (searchTerm === '') {
            items.forEach(item => {
                item.style.display = 'block';
                item.classList.remove('destaque-pesquisa');
            });
            updateCounter(items.length);

            if (typeof window.updateItemCount === 'function') {
                window.updateItemCount();
            }
            return;
        }

        let matchCount = 0;

        items.forEach(item => {
            const nomeElement = item.querySelector('.item-nome');
            const tipoElement = item.querySelector('.item-tipo');

            const nome = nomeElement ? nomeElement.textContent.toLowerCase() : '';
            const tipo = tipoElement ? tipoElement.textContent.toLowerCase() : '';

            const matches = nome.includes(searchTerm) || tipo.includes(searchTerm);

            if (matches) {
                item.style.display = 'block';
                matchCount++;

                if (nome === searchTerm || tipo === searchTerm) {
                    item.classList.add('destaque-pesquisa');
                    setTimeout(() => {
                        item.classList.remove('destaque-pesquisa');
                    }, 1000);
                }
            } else {
                item.style.display = 'none';
            }
        });

        updateCounter(matchCount);

        if (typeof window.updateItemCount === 'function') {
            window.updateItemCount();
        }
    }

    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 150);
    });

    searchClear.addEventListener('click', function () {
        searchInput.value = '';
        searchInput.focus();
        performSearch();
    });

    updateCounter(items.length);
});

// ===== ALTERNAR VISUALIZAÇÃO (GRID/LISTA) =====
document.addEventListener('DOMContentLoaded', function () {
    const viewGrid = document.getElementById('view-grid');
    const viewList = document.getElementById('view-list');
    const listagemContainer = document.querySelector('.listagem-itens');
    const totalItensSpan = document.getElementById('view-total-itens');

    window.updateItemCount = function () {
        const visibleItems = document.querySelectorAll('.item-link:not([style*="display: none"])').length;
        totalItensSpan.textContent = visibleItems;
    };

    const savedView = localStorage.getItem('viewMode') || 'grid';
    setViewMode(savedView);

    viewGrid.addEventListener('click', function () {
        setViewMode('grid');
    });

    viewList.addEventListener('click', function () {
        setViewMode('list');
    });

    function setViewMode(mode) {
        viewGrid.classList.toggle('active', mode === 'grid');
        viewList.classList.toggle('active', mode === 'list');

        if (mode === 'list') {
            listagemContainer.classList.add('view-list');
        } else {
            listagemContainer.classList.remove('view-list');
        }

        localStorage.setItem('viewMode', mode);

        setTimeout(window.updateItemCount, 50);
    }

    const searchInput = document.getElementById('pesquisa-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            setTimeout(window.updateItemCount, 200);
        });
    }

    window.updateItemCount();

    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.attributeName === 'style') {
                window.updateItemCount();
            }
        });
    });

    document.querySelectorAll('.item-link').forEach(item => {
        observer.observe(item, { attributes: true });
    });
});

// ===== ORDENAÇÃO =====
document.addEventListener('DOMContentLoaded', function () {
    const ordenacaoBotoes = {
        nome: document.getElementById('ordenar-nome'),
        tipo: document.getElementById('ordenar-tipo'),
        tamanho: document.getElementById('ordenar-tamanho'),
        data: document.getElementById('ordenar-data')
    };

    if (!ordenacaoBotoes.nome) {
        console.log('Botões de ordenação não encontrados');
        return;
    }

    let ordenacaoAtual = {
        criterio: 'tipo',
        ordem: 'asc'
    };

    let isOrdenando = false;

    try {
        const savedOrdenacao = localStorage.getItem('ordenacao');
        if (savedOrdenacao) {
            ordenacaoAtual = JSON.parse(savedOrdenacao);
        }
    } catch (e) {
        console.error('Erro ao carregar ordenação salva:', e);
    }

    function atualizarBotoesOrdenacao() {
        Object.values(ordenacaoBotoes).forEach(btn => {
            if (btn) {
                btn.classList.remove('active');
            }
        });

        const btnAtual = ordenacaoBotoes[ordenacaoAtual.criterio];
        if (btnAtual) {
            btnAtual.classList.add('active');
            btnAtual.setAttribute('data-ordem', ordenacaoAtual.ordem);
        }
    }

    function parseTamanho(tamanhoTexto) {
        if (!tamanhoTexto || tamanhoTexto === '--') return 0;

        const match = tamanhoTexto.match(/([\d.]+)\s*(\w+)/);
        if (!match) return 0;

        const [_, valor, unidade] = match;
        const unidades = { 'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4 };
        return parseFloat(valor) * (unidades[unidade] || 1);
    }

    function parseData(dataTexto) {
        if (!dataTexto) return 0;

        if (dataTexto.includes('Hoje')) {
            const hora = dataTexto.match(/(\d{2}):(\d{2})/);
            if (hora) {
                const hoje = new Date();
                hoje.setHours(parseInt(hora[1]), parseInt(hora[2]), 0);
                return hoje.getTime();
            }
        } else if (dataTexto.includes('Ontem')) {
            const hora = dataTexto.match(/(\d{2}):(\d{2})/);
            if (hora) {
                const ontem = new Date();
                ontem.setDate(ontem.getDate() - 1);
                ontem.setHours(parseInt(hora[1]), parseInt(hora[2]), 0);
                return ontem.getTime();
            }
        } else {
            const partes = dataTexto.match(/(\d{2})\/(\d{2})\/(\d{4})\s+(\d{2}):(\d{2})/);
            if (partes) {
                const [_, dia, mes, ano, hora, min] = partes;
                return new Date(ano, mes - 1, dia, hora, min).getTime();
            }
        }
        return 0;
    }

    function ordenarItens() {
        if (isOrdenando) return;

        const container = document.querySelector('.listagem-itens');
        if (!container) return;

        const items = Array.from(container.querySelectorAll('.item-link'));
        if (items.length === 0) return;

        isOrdenando = true;

        items.sort((a, b) => {
            let valorA, valorB;

            switch (ordenacaoAtual.criterio) {
                case 'nome':
                    const nomeA = a.querySelector('.item-nome')?.textContent || '';
                    const nomeB = b.querySelector('.item-nome')?.textContent || '';
                    valorA = nomeA.toLowerCase();
                    valorB = nomeB.toLowerCase();
                    break;

                case 'tipo':
                    const getTipoPeso = (item) => {
                        if (item.querySelector('.item-pasta')) return 1;
                        if (item.querySelector('.item-imagem')) return 2;
                        if (item.querySelector('.item-audio')) return 3;
                        return 4;
                    };
                    valorA = getTipoPeso(a);
                    valorB = getTipoPeso(b);
                    break;

                case 'tamanho':
                    if (a.querySelector('.item-pasta')) {
                        valorA = Infinity;
                    } else {
                        const tamanhoA = a.querySelector('.item-tamanho')?.textContent || '0 B';
                        valorA = parseTamanho(tamanhoA);
                    }

                    if (b.querySelector('.item-pasta')) {
                        valorB = Infinity;
                    } else {
                        const tamanhoB = b.querySelector('.item-tamanho')?.textContent || '0 B';
                        valorB = parseTamanho(tamanhoB);
                    }
                    break;

                case 'data':
                    if (a.querySelector('.item-pasta')) {
                        valorA = Infinity;
                    } else {
                        const dataA = a.querySelector('.item-data')?.textContent || '';
                        valorA = parseData(dataA);
                    }

                    if (b.querySelector('.item-pasta')) {
                        valorB = Infinity;
                    } else {
                        const dataB = b.querySelector('.item-data')?.textContent || '';
                        valorB = parseData(dataB);
                    }
                    break;

                default:
                    return 0;
            }

            let comparacao = 0;
            if (typeof valorA === 'string' && typeof valorB === 'string') {
                comparacao = valorA.localeCompare(valorB);
            } else {
                comparacao = valorA - valorB;
            }

            return ordenacaoAtual.ordem === 'asc' ? comparacao : -comparacao;
        });

        items.forEach(item => container.appendChild(item));

        setTimeout(() => {
            isOrdenando = false;
        }, 100);

        if (typeof window.updateItemCount === 'function') {
            window.updateItemCount();
        }
    }

    Object.entries(ordenacaoBotoes).forEach(([criterio, btn]) => {
        if (btn) {
            btn.addEventListener('click', function () {
                const clicouNoMesmo = ordenacaoAtual.criterio === criterio;

                if (clicouNoMesmo) {
                    ordenacaoAtual.ordem = ordenacaoAtual.ordem === 'asc' ? 'desc' : 'asc';
                } else {
                    ordenacaoAtual.criterio = criterio;
                    ordenacaoAtual.ordem = 'asc';
                }

                try {
                    localStorage.setItem('ordenacao', JSON.stringify(ordenacaoAtual));
                } catch (e) {
                    console.error('Erro ao salvar ordenação:', e);
                }

                atualizarBotoesOrdenacao();
                ordenarItens();
            });
        }
    });

    const searchInput = document.getElementById('pesquisa-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            setTimeout(ordenarItens, 250);
        });
    }

    const container = document.querySelector('.listagem-itens');
    if (container) {
        let timeoutId = null;

        const observer = new MutationObserver(function (mutations) {
            if (isOrdenando) return;

            const foiPesquisa = mutations.some(m =>
                m.type === 'attributes' && m.attributeName === 'style'
            );

            if (foiPesquisa) {
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }

                timeoutId = setTimeout(() => {
                    ordenarItens();
                    timeoutId = null;
                }, 150);
            }
        });

        observer.observe(container, {
            childList: true,
            attributes: true,
            subtree: true,
            attributeFilter: ['style']
        });
    }

    setTimeout(() => {
        atualizarBotoesOrdenacao();
        ordenarItens();
    }, 100);
});

// ===== NAVEGAÇÃO SIMPLES DOS CARDS =====
document.addEventListener('DOMContentLoaded', function () {
    // Para cada card de pasta
    document.querySelectorAll('[data-tipo="pasta"]').forEach(card => {
        card.addEventListener('click', function (e) {
            // Se clicou em checkbox ou botões, não navega
            if (e.target.closest('.item-checkbox') ||
                e.target.closest('.item-checkbox-input') ||
                e.target.closest('.botao-download') ||
                e.target.closest('.botao-excluir') ||
                e.target.closest('form') ||
                e.target.closest('button')) {
                return;
            }

            const caminho = this.dataset.caminho;
            if (caminho) {
                window.location.href = `/explorar/${caminho}`;
            }
        });
    });

    // Para imagens (lightbox)
    document.querySelectorAll('[data-tipo="imagem"]').forEach(card => {
        card.addEventListener('click', function (e) {
            if (e.target.closest('.item-checkbox') ||
                e.target.closest('.item-checkbox-input') ||
                e.target.closest('.botao-download') ||
                e.target.closest('.botao-excluir') ||
                e.target.closest('form') ||
                e.target.closest('button')) {
                return;
            }

            // Disparar o lightbox (já existe)
            const imgCard = this.querySelector('.item-imagem');
            if (imgCard) {
                const event = new MouseEvent('click', { bubbles: true });
                imgCard.dispatchEvent(event);
            }
        });
    });

    // Para áudios
    document.querySelectorAll('[data-tipo="audio"]').forEach(card => {
        card.addEventListener('click', function (e) {
            if (e.target.closest('.item-checkbox') ||
                e.target.closest('.item-checkbox-input') ||
                e.target.closest('.botao-download') ||
                e.target.closest('.botao-excluir') ||
                e.target.closest('form') ||
                e.target.closest('button') ||
                e.target.closest('audio')) {
                return;
            }

            const caminho = this.dataset.caminho;
            if (caminho) {
                window.location.href = `/visualizar/${caminho}`;
            }
        });
    });

    // Para arquivos comuns
    document.querySelectorAll('[data-tipo="arquivo"]').forEach(card => {
        card.addEventListener('click', function (e) {
            if (e.target.closest('.item-checkbox') ||
                e.target.closest('.item-checkbox-input') ||
                e.target.closest('.botao-download') ||
                e.target.closest('.botao-excluir') ||
                e.target.closest('form') ||
                e.target.closest('button')) {
                return;
            }

            const caminho = this.dataset.caminho;
            if (caminho) {
                window.location.href = `/download/${caminho}`;
            }
        });
    });
});

// ===== SELEÇÃO MÚLTIPLA =====
document.addEventListener('DOMContentLoaded', function () {
    const selecaoBarra = document.getElementById('selecao-barra');
    const selecaoContador = document.getElementById('selecao-contador');
    const selecaoSelectAll = document.getElementById('selecao-select-all');
    const selecaoClear = document.getElementById('selecao-clear');
    const selecaoDelete = document.getElementById('selecao-delete');
    const selecaoDownload = document.getElementById('selecao-download');

    let itensSelecionados = new Set();
    let processandoObserver = false;

    function atualizarSelecao() {
        const count = itensSelecionados.size;
        selecaoContador.textContent = count;
        selecaoBarra.style.display = count > 0 ? 'flex' : 'none';

        document.querySelectorAll('.item-link').forEach(item => {
            const caminho = item.dataset.caminho;
            if (itensSelecionados.has(caminho)) {
                item.classList.add('selecionado');
            } else {
                item.classList.remove('selecionado');
            }
        });
    }

    // Função para configurar eventos nos checkboxes
    function configurarCheckbox(checkbox) {
        // Remove eventos antigos (se houver)
        checkbox.removeEventListener('change', handleCheckboxChange);
        // Adiciona evento novo
        checkbox.addEventListener('change', handleCheckboxChange);
    }

    // Handler separado para o evento change
    function handleCheckboxChange(e) {
        e.stopPropagation();
        const checkbox = e.target;
        const caminho = checkbox.dataset.caminho;
        const item = checkbox.closest('.item-link');

        if (checkbox.checked) {
            itensSelecionados.add(caminho);
            item.classList.add('selecionado');
        } else {
            itensSelecionados.delete(caminho);
            item.classList.remove('selecionado');
        }

        atualizarSelecao();
    }

    // Configurar todos os checkboxes existentes
    document.querySelectorAll('.item-checkbox-input').forEach(configurarCheckbox);

    // Botão selecionar todos
    selecaoSelectAll.addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('.item-checkbox-input');
        const todosSelecionados = Array.from(checkboxes).every(cb => cb.checked);

        checkboxes.forEach(checkbox => {
            checkbox.checked = !todosSelecionados;
            const caminho = checkbox.dataset.caminho;
            const item = checkbox.closest('.item-link');

            if (!todosSelecionados) {
                itensSelecionados.add(caminho);
                item.classList.add('selecionado');
            } else {
                itensSelecionados.delete(caminho);
                item.classList.remove('selecionado');
            }
        });

        atualizarSelecao();
    });

    // Botão limpar seleção
    selecaoClear.addEventListener('click', function () {
        document.querySelectorAll('.item-checkbox-input').forEach(checkbox => {
            checkbox.checked = false;
            checkbox.closest('.item-link').classList.remove('selecionado');
        });

        itensSelecionados.clear();
        atualizarSelecao();
    });

    // Botão deletar selecionados - VERSÃO COM TOAST
    selecaoDelete.addEventListener('click', async function (e) {
        e.stopPropagation();

        if (itensSelecionados.size === 0) return;

        const mensagem = itensSelecionados.size === 1
            ? 'Tem certeza que deseja excluir este item?'
            : `Tem certeza que deseja excluir ${itensSelecionados.size} itens?`;

        const detalhe = Array.from(itensSelecionados).slice(0, 5).join('\n');
        const detalheCompleto = itensSelecionados.size > 5
            ? `${detalhe}\n... e mais ${itensSelecionados.size - 5} itens`
            : detalhe;

        const confirmado = await ConfirmModal.open({
            title: 'Excluir itens selecionados',
            message: mensagem,
            detail: detalheCompleto
        });

        if (!confirmado) return;

        // Mostrar loading no botão
        const textoOriginal = selecaoDelete.innerHTML;
        selecaoDelete.disabled = true;
        selecaoDelete.innerHTML = '<span class="selecao-icon">⏳</span> Excluindo...';

        try {
            const response = await fetch('/deletar_multiplos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    caminhos: Array.from(itensSelecionados)
                })
            });

            const resultado = await response.json();

            if (resultado.sucesso) {
                // Mostrar toast de sucesso
                if (resultado.erros && resultado.erros.length > 0) {
                    showToast(`✅ ${resultado.excluidos} itens excluídos\n❌ ${resultado.erros.length} falhas`, 'warning');
                } else {
                    showToast(`✅ ${resultado.excluidos} itens excluídos com sucesso!`, 'success');
                }

                // Recarregar a página após um pequeno delay
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                showToast(`Erro: ${resultado.erro}`, 'error');
            }
        } catch (error) {
            console.error('Erro na exclusão:', error);
            showToast('Erro ao excluir itens. Tente novamente.', 'error');
        } finally {
            // Restaurar botão
            selecaoDelete.disabled = false;
            selecaoDelete.innerHTML = textoOriginal;
        }
    });

    // Botão download ZIP (substitua o placeholder existente)
    selecaoDownload.addEventListener('click', function () {
        if (itensSelecionados.size === 0) return;

        // Criar formulário dinamicamente
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = "{{ url_for('file.download_zip') }}";
        form.style.display = 'none';

        // Adicionar cada caminho selecionado como input
        itensSelecionados.forEach(caminho => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'caminhos';
            input.value = caminho;
            form.appendChild(input);
        });

        // Adicionar formulário ao body e submeter
        document.body.appendChild(form);
        form.submit();

        // Limpar o formulário após o envio
        setTimeout(() => {
            document.body.removeChild(form);
        }, 1000);
    });

    // ===== ATALHOS DE TECLADO =====

    // Ctrl+A para selecionar todos
    document.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.key === 'a') {
            e.preventDefault();
            e.stopPropagation();
            selecaoSelectAll.click();
        }
    });

    // Delete para excluir selecionados
    document.addEventListener('keydown', function (e) {
        // Verifica se a tecla pressionada é Delete
        if (e.key === 'Delete' || e.key === 'Del') {
            // Verifica se há itens selecionados
            if (itensSelecionados.size > 0) {
                // Verifica se não está digitando em um input
                const tag = e.target.tagName.toLowerCase();
                if (tag !== 'input' && tag !== 'textarea' && !e.target.isContentEditable) {
                    e.preventDefault();
                    e.stopPropagation();
                    // Disparar o clique no botão deletar
                    selecaoDelete.click();
                }
            }
        }
    });

    // Observer para novos checkboxes (pesquisa/ordenação) - VERSÃO SEM LOOP
    const observer = new MutationObserver(function (mutations) {
        // Evitar processamento múltiplo
        if (processandoObserver) return;
        processandoObserver = true;

        let temNovosCheckboxes = false;

        mutations.forEach(mutation => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Elemento
                        // Verificar se o nó adicionado é um checkbox ou contém checkboxes
                        if (node.classList && node.classList.contains('item-checkbox-input')) {
                            temNovosCheckboxes = true;
                        } else if (node.querySelectorAll) {
                            if (node.querySelectorAll('.item-checkbox-input').length > 0) {
                                temNovosCheckboxes = true;
                            }
                        }
                    }
                });
            }
        });

        if (temNovosCheckboxes) {
            // Configurar apenas os novos checkboxes, sem recriar tudo
            document.querySelectorAll('.item-checkbox-input').forEach(checkbox => {
                // Verificar se já tem o evento (forma simples de evitar duplicação)
                if (!checkbox.hasAttribute('data-event-configurado')) {
                    configurarCheckbox(checkbox);
                    checkbox.setAttribute('data-event-configurado', 'true');
                }
            });
        }

        // Liberar flag após um pequeno delay
        setTimeout(() => {
            processandoObserver = false;
        }, 100);
    });

    const container = document.querySelector('.listagem-itens');
    if (container) {
        observer.observe(container, { childList: true, subtree: true });
    }
});

// ===== ÍCONES DINÂMICOS (FALLBACK) =====
document.addEventListener('DOMContentLoaded', function () {
    // Para ícones que não foram pegos pelo CSS, podemos adicionar lógica JS
    document.querySelectorAll('.file-icon').forEach(icon => {
        const extensao = icon.dataset.extensao;
        if (!extensao) return;

        // Mapeamento de extensões para ícones (fallback)
        const iconMap = {
            'pdf': '📕', 'doc': '📘', 'docx': '📘', 'xls': '📊', 'xlsx': '📊',
            'ppt': '📽️', 'pptx': '📽️', 'txt': '📃', 'rtf': '📄',
            'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️', 'svg': '🖼️',
            'mp3': '🎵', 'wav': '🎵', 'ogg': '🎵', 'flac': '🎵',
            'mp4': '🎬', 'avi': '🎬', 'mkv': '🎬', 'mov': '🎬',
            'zip': '📦', 'rar': '📦', '7z': '📦', 'tar': '📦', 'gz': '📦',
            'html': '🌐', 'htm': '🌐', 'css': '🎨', 'js': '⚡', 'py': '🐍',
            'java': '☕', 'c': '⚙️', 'cpp': '⚙️', 'php': '🐘', 'json': '📋',
            'exe': '⚙️', 'msi': '⚙️', 'bat': '📜', 'sh': '📜',
            'sql': '🗄️', 'db': '🗄️', 'sqlite': '🗄️'
        };

        // Se a extensão existir no mapa, substituir o conteúdo
        if (iconMap[extensao]) {
            // Só substitui se o ícone atual for o padrão 📄
            if (icon.textContent === '📄') {
                icon.textContent = iconMap[extensao];
            }
        }
    });
});

// ===== SALVAR POSIÇÃO DA ROLAGEM =====
(function () {
    // Salvar posição antes de sair da página
    window.addEventListener('beforeunload', function () {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    });

    // Restaurar posição quando a página carregar
    window.addEventListener('load', function () {
        const savedPosition = sessionStorage.getItem('scrollPosition');
        if (savedPosition) {
            // Pequeno delay para garantir que a página renderizou
            setTimeout(function () {
                window.scrollTo(0, parseInt(savedPosition));
                sessionStorage.removeItem('scrollPosition'); // Limpar depois de usar
            }, 100);
        }
    });
})();

document.addEventListener('DOMContentLoaded', function () {
    const overlay = document.getElementById('global-drop-overlay');
    const progressContainer = document.getElementById('upload-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');

    let dragCounter = 0;

    // 🔥 Detecta entrada de arquivos
    document.addEventListener('dragenter', (e) => {
        if (e.dataTransfer.types.includes('Files')) {
            dragCounter++;
            overlay.classList.add('active');
        }
    });

    document.addEventListener('dragleave', () => {
        dragCounter--;
        if (dragCounter <= 0) {
            overlay.classList.remove('active');
        }
    });

    document.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    document.addEventListener('drop', (e) => {
        e.preventDefault();

        overlay.classList.remove('active');
        dragCounter = 0;

        const files = e.dataTransfer.files;
        uploadFiles(files);
    });

    function uploadFiles(files) {
        if (!files.length) return;

        const panel = document.getElementById('upload-panel');
        const list = document.getElementById('upload-list');

        panel.style.display = 'flex';

        const caminho = window.location.pathname.replace('/explorar', '');

        Array.from(files).forEach(file => {
            const item = document.createElement('div');
            item.className = 'upload-item';

            item.innerHTML = `
            <div class="upload-name">${file.name}</div>
            <div class="upload-bar">
                <div class="upload-fill"></div>
            </div>
            <div class="upload-status">Enviando...</div>
        `;

            list.appendChild(item);

            const fill = item.querySelector('.upload-fill');
            const status = item.querySelector('.upload-status');

            const formData = new FormData();
            formData.append('arquivo', file);

            const xhr = new XMLHttpRequest();
            xhr.open('POST', `/upload${caminho}`, true);

            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    fill.style.width = percent + '%';
                }
            });

            xhr.onload = () => {
                if (xhr.status === 200) {
                    fill.style.width = '100%';
                    status.textContent = 'Concluído';
                    item.classList.add('success');

                    showToast(`"${file.name}" enviado`, 'success');
                } else {
                    status.textContent = 'Erro no upload';
                    item.classList.add('error');

                    showToast(`Erro ao enviar "${file.name}"`, 'error');
                }
            };

            xhr.onerror = () => {
                status.textContent = 'Erro de conexão';
                item.classList.add('error');

                showToast(`Erro de conexão`, 'error');
            };

            xhr.send(formData);
        });

        // 🔥 Atualiza depois de tudo
        setTimeout(() => {
            atualizarLista();
        }, 800);
    }
});

function fecharPainel() {
    document.getElementById('upload-panel').style.display = 'none';
}

async function atualizarLista() {
    const container = document.getElementById('file-list-container');

    const caminho = window.location.pathname.replace('/explorar', '');
    const response = await fetch(`/partial/lista${caminho}`);

    const html = await response.text();

    container.innerHTML = html;

    showToast('Atualizado!', 'info');
}