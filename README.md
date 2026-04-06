# ☁️ Cloud Storage App (Self-Hosted Drive)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()

> 🚀 Um sistema de armazenamento em nuvem self-hosted, inspirado no Google Drive, com interface moderna, uploads avançados e foco em **segurança, simplicidade e controle total dos dados**.

---

## 📌 Sobre o Projeto

O **Cloud Storage App** é uma aplicação web desenvolvida com **Python (Flask)** que transforma seu computador em um servidor de arquivos acessível via navegador. O projeto evoluiu para oferecer uma experiência cada vez mais próxima de serviços como o Google Drive, com recursos modernos como **drag & drop, upload com progresso em tempo real, player de áudio integrado e atualização dinâmica da interface**, mantendo o principal objetivo:

> 🔒 Garantir ao usuário **controle total sobre seus dados**, sem dependência de serviços terceiros.

---

## ✨ Funcionalidades Implementadas (+25)

### 🔐 Segurança & Autenticação
*   **Sistema de Login:** Proteção contra força bruta com rate limiting agressivo.
*   **Senhas Seguras:** Armazenamento com hash (scrypt/pbkdf2).
*   **Sessões Blindadas:** Cookies `HttpOnly`, `SameSite=Lax` e `Secure` (em produção).
*   **Headers de Segurança:** CSP (Content Security Policy), HSTS, X-Frame-Options e X-Content-Type-Options.
*   **Proteção de Rotas:** Validação contra ataques de *path traversal* e CSRF em todas as operações de escrita.

### 📂 Gerenciamento de Arquivos
*   **Navegação Completa:** Diretórios com breadcrumb interativo.
*   **Upload Avançado:** Múltiplos arquivos via botão ou **Drag & Drop global**.
*   **Painel de Uploads:** Progresso individual em tempo real (estilo Google Drive).
*   **Downloads:** Individual ou em lote compactado em **ZIP**.
*   **Pastas:** Criação e exclusão de diretórios.
*   **Seleção Múltipla:** Atalhos de teclado (`Ctrl+A`, `Delete`, `Ctrl+Clique`).

### ⚡ Experiência do Usuário (UX)
*   **Interface AJAX:** Atualização da lista de arquivos e exclusão individual **sem recarregar a página**.
*   **Tema Híbrido:** Claro/Escuro persistente no `localStorage`.
*   **Visualização:** Lightbox para imagens, player de áudio integrado e visualizador de PDF.
*   **Organização:** Pesquisa em tempo real e ordenação por nome, tipo, tamanho ou data.
*   **Responsividade:** Interface adaptada para Desktop, Tablet e Mobile.
*   **Feedback Visual:** Toast notifications e modais de confirmação personalizados.

---

## 🚀 Como Instalar e Executar

### 1. Preparação
```bash
git clone https://github.com/PointycarlosE/cloud-storage-app.git
cd cloud-storage-app
```

### 2. Ambiente Virtual
```bash
python -m venv venv
# Ativar (Windows): venv\Scripts\activate
# Ativar (Linux/Mac/Termux): source venv/bin/activate
```

### 3. Instalação
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração e Modos de Uso

O sistema utiliza um arquivo `.env` dentro da pasta `instance/` para se configurar automaticamente.

### 🏠 Modo Local (Desenvolvimento)
Ideal para usar em casa via Wi-Fi ou para testes.
1.  No arquivo `instance/.env`, defina `FLASK_ENV=development`.
2.  Execute: `python run.py`
3.  Acesse: `http://localhost:5000` ou `http://SEU_IP_LOCAL:5000`

### 🌐 Modo Internet (Produção)
Ideal para acessar de qualquer lugar via Cloudflare Tunnel ou VPS.
1.  No arquivo `instance/.env`, defina `FLASK_ENV=production`.
2.  **Use o Gunicorn** (já pré-configurado no projeto):
    ```bash
    gunicorn -c gunicorn_config.py app:app
    ```
3.  O sistema ativará automaticamente a blindagem máxima (HTTPS obrigatório, HSTS rígido, etc).

---

## 📱 Rodando no Celular (Termux)
Este projeto é otimizado para rodar em dispositivos Android antigos!
1.  Instale o Termux e execute: `pkg install python cloudflared`
2.  Siga os passos de instalação acima.
3.  Use o **Cloudflare Tunnel** para criar um link seguro (HTTPS) sem abrir portas no roteador.

---

## 🛠️ Estrutura do Projeto
```
cloud-storage-app/
├── app/                # Backend (Flask)
├── frontend/           # Interface (HTML, CSS, JS)
├── instance/           # Configurações locais (.env) e Logs
├── gunicorn_config.py  # Configuração para servidor de produção
├── run.py              # Inicialização para modo local
└── requirements.txt    # Dependências
```

---

## 🌍 Visão de Futuro & Roadmap

O objetivo final é oferecer uma alternativa gratuita, segura e autônoma a serviços como Google Drive e Dropbox.

### 🔥 Concluído Recentemente
*   [x] Exclusão individual sem reload (AJAX)
*   [x] Blindagem contra Drag & Drop interno acidental
*   [x] Correção de carregamento de miniaturas pós-AJAX
*   [x] Modo Híbrido (Local/Produção) e Gunicorn Config

### 🚀 Próximos Passos
*   [ ] **Compartilhamento por link:** Gerar links temporários para terceiros.
*   [ ] **Sistema Multiusuário:** Espaços individuais e permissões.
*   [ ] **Logs de Atividade:** Interface de auditoria para o administrador.
*   [ ] **Visualização de Vídeos:** Player integrado em modal.
*   [ ] **2FA:** Autenticação de dois fatores para segurança máxima.

---

## 🤝 Contribuição
1. Fork o projeto | 2. Crie uma branch | 3. Commit mudanças | 4. Abra um Pull Request

---

## 📝 Licença
Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor
**Carlos** - [GitHub](https://github.com/PointycarlosE)

Se este projeto te ajudou, considere deixar uma estrela ⭐ no repositório!
