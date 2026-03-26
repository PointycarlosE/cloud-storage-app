# ☁️ Cloud Storage App (Self-Hosted Drive)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()

> 🚀 Um sistema de armazenamento em nuvem self-hosted, inspirado no Google Drive, com interface moderna, uploads avançados e foco em **segurança, simplicidade e controle total dos dados**.

---

## 📌 Sobre o Projeto

O **Cloud Storage App** é uma aplicação web desenvolvida com **Python (Flask)** que transforma seu computador em um servidor de arquivos acessível via navegador.

O projeto evoluiu para oferecer uma experiência cada vez mais próxima de serviços como o Google Drive, com recursos modernos como **drag & drop, upload com progresso em tempo real, player de áudio integrado e atualização dinâmica da interface**, mantendo o principal objetivo:

> 🔒 Garantir ao usuário **controle total sobre seus dados**, sem dependência de serviços terceiros.

---

## ✨ Funcionalidades

### 🔐 Segurança & Autenticação

* Sistema de login com proteção contra força bruta
* Senhas armazenadas com hash seguro (scrypt/pbkdf2)
* Sessões protegidas (HttpOnly + SameSite)
* Proteção de rotas e controle de acesso
* Validação contra ataques de path traversal

---

### 📂 Gerenciamento de Arquivos

* Navegação completa por diretórios
* Upload de múltiplos arquivos
* Upload via **drag & drop em toda a interface**
* Painel de uploads com progresso individual (estilo Google Drive)
* Download individual e em ZIP
* Criação e exclusão de pastas
* Seleção múltipla com atalhos (`Ctrl + A`, `Delete`)

---

### ⚡ Experiência Dinâmica (UX)

* Atualização de arquivos **sem reload (AJAX)**
* Interface fluida (mantém contexto e scroll)
* Feedback em tempo real durante uploads
* Estados de upload:

  * Enviando
  * Concluído
  * Erro

---

### 🔍 Organização & Busca

* Pesquisa em tempo real
* Ordenação por nome, tipo, tamanho e data
* Exibição de metadados formatados
* Breadcrumb interativo

---

### 🎨 Interface

* Novo layout moderno e mais elegante
* Interface refinada com melhor organização visual
* Tema claro/escuro persistente
* Visualização em lista ou grade
* Design responsivo (desktop, tablet e mobile)
* Toast notifications modernas
* Modais personalizados
* Scrollbars customizadas (tema claro/escuro)
* Painel de uploads estilizado e animado
---

### 🖼️ Visualização de Arquivos

* Lightbox para imagens
* 🎵 Player de áudio integrado (reprodução direta no navegador)
* Visualização de PDF
* Miniaturas automáticas
---

### 🎵 Reprodução de Áudio

* Player de áudio integrado na interface
* Reprodução direta de arquivos (.mp3, .wav, etc.)
* Controles nativos (play, pause, progresso)
* Experiência fluida sem necessidade de download

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/PointycarlosE/cloud-storage-app.git
cd cloud-storage-app
```

---

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Execute o projeto

```bash
python run.py
```

Acesse:

```
http://localhost:5000
```

---

## ⚙️ Primeira Execução

* Crie sua conta ao acessar o sistema
* Defina a pasta base dos arquivos
* Reinicie o servidor (temporariamente necessário)

---

## 🌐 Acesso na Rede Local

1. Descubra seu IP:

```bash
ipconfig      # Windows  
ifconfig      # Linux/Mac  
```

2. Acesse:

```
http://SEU_IP:5000
```

> ⚠️ Verifique se o firewall permite conexões na porta.

---

## 🛠️ Estrutura do Projeto

```
cloud-storage-app/
├── app/            # Backend (Flask)
├── frontend/       # Interface (HTML, CSS, JS)
├── instance/       # Configurações locais (.env)
├── run.py          # Inicialização da aplicação
├── requirements.txt
```

---

## 🔧 Configuração

### Variáveis de ambiente (.env)

```env
PASTA_BASE=/caminho/para/arquivos
SECRET_KEY=sua_chave_secreta
```

---

### Alterar porta

```python
PORT = 8080  # padrão: 5000
```

---

## 📦 Tecnologias Utilizadas

* **Backend:** Python + Flask
* **Frontend:** HTML, CSS, JavaScript
* **Segurança:** Flask-Login, Werkzeug
* **Configuração:** python-dotenv

---

## 🌍 Visão de Futuro

O projeto está sendo desenvolvido para evoluir de um sistema local para uma solução completa acessível pela internet, mantendo como pilares:

* 🔒 Segurança
* ⚙️ Simplicidade
* 🧠 Autonomia do usuário

O objetivo é permitir que qualquer pessoa possa hospedar seu próprio sistema de armazenamento e acessá-lo de qualquer lugar com facilidade.

---

### 🔐 Segurança como Prioridade

A disponibilização externa exige um alto nível de proteção. Por isso, a segurança é tratada como prioridade central no desenvolvimento.

Entre os pontos em evolução:

* Implementação de HTTPS (SSL/TLS)
* Proteção contra CSRF e XSS
* Rate limiting global
* Autenticação em dois fatores (2FA)
* Logs e auditoria de acessos
* Controle de permissões (multiusuário)

> ⚠️ Atualmente, o uso é recomendado em rede local até que os requisitos de segurança para acesso externo estejam totalmente implementados.

---

### 🚧 Desafios Atuais

* Deploy em ambiente externo (VPS / cloud)
* Configuração de domínio e acesso remoto
* Suporte a múltiplos usuários simultâneos
* Automatização da instalação

---

### 🎯 Objetivo Final

Criar uma plataforma que seja:

* 🔒 Segura por padrão
* ⚙️ Simples de instalar
* 🌐 Acessível de qualquer lugar
* 🧠 Independente de serviços terceiros

---

## 🚧 Roadmap

### 🔥 Concluído recentemente

* [x] Upload com barra de progresso
* [x] Drag & Drop global
* [x] Painel de uploads
* [x] Atualização dinâmica sem reload
* [x] Player de áudio integrado
* [x] Novo layout moderno

---

### 🚀 Próximos passos

* [ ] Compartilhamento por link
* [ ] Sistema multiusuário
* [ ] Logs de atividade
* [ ] Upload de pastas
* [ ] Exclusão dinâmica sem reload
* [ ] Deploy online seguro

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`feature/minha-feature`)
3. Commit (`git commit -m 'feat: nova feature'`)
4. Push (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

**Carlos**
GitHub: https://github.com/PointycarlosE

---

## ⭐ Apoio

Se este projeto te ajudou ou te inspirou, considere deixar uma estrela ⭐ no repositório!
