# ☁️ Cloud Storage App (Self-Hosted Drive)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()

> 🚀 Um sistema de armazenamento em nuvem local, inspirado no Google Drive, que permite gerenciar arquivos diretamente pelo navegador com foco em segurança, simplicidade e controle total dos dados.

---

## 📌 Sobre o Projeto

O **Cloud Storage App** é uma aplicação web self-hosted desenvolvida com **Python (Flask)** que transforma seu computador em um servidor de arquivos acessível via navegador.

O projeto surgiu com o objetivo de oferecer uma alternativa pessoal aos serviços de armazenamento em nuvem tradicionais, permitindo que o usuário tenha **controle total sobre seus arquivos**, sem depender de terceiros.

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
* Download individual e em ZIP
* Criação de pastas
* Exclusão de arquivos e diretórios
* Seleção múltipla com atalhos (`Ctrl + A`, `Delete`)

---

### 🔍 Organização & Busca

* Pesquisa em tempo real
* Ordenação por nome, tipo, tamanho e data
* Exibição de metadados formatados
* Breadcrumb interativo

---

### 🎨 Interface

* Tema claro/escuro persistente
* Visualização em lista ou grade
* Design responsivo (desktop, tablet e mobile)
* Toast notifications e modais personalizados

---

### 🖼️ Visualização de Arquivos

* Lightbox para imagens
* Player de áudio integrado
* Visualização de PDF
* Miniaturas automáticas

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/cloud-storage-app.git
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

* Crie sua conta ao acessar o sistema pela primeira vez
* Defina a pasta base onde os arquivos serão armazenados
* Reinicie o servidor (temporariamente necessário)

---

## 🌐 Acesso na Rede Local

1. Descubra o IP do seu computador:

```bash
ipconfig      # Windows
ifconfig      # Linux/Mac
```

2. Acesse de outro dispositivo:

```
http://SEU_IP:5000
```

> ⚠️ Verifique se o firewall permite conexões na porta utilizada.

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
PASTA_BASE=/caminho/para/seus/arquivos
SECRET_KEY=sua_chave_secreta
```

---

### Alterar porta (config.py)

```python
PORT = 8080 # PADRÃO 5000
```

---

## 📦 Tecnologias Utilizadas

* **Backend:** Python + Flask
* **Frontend:** HTML, CSS, JavaScript
* **Segurança:** Flask-Login, Werkzeug
* **Configuração:** python-dotenv

---

## 🌍 Visão de Futuro

O objetivo deste projeto é evoluir de um sistema local para uma solução completa acessível pela internet, mantendo como pilares a **segurança, simplicidade e autonomia do usuário**.

A ideia é permitir que qualquer pessoa possa hospedar seu próprio sistema de armazenamento e acessá-lo de qualquer lugar, sem depender de serviços terceiros.

---

### 🔐 Segurança como Prioridade

A disponibilização em ambiente externo exige um nível elevado de proteção. Por isso, o projeto está sendo desenvolvido com foco contínuo em segurança.

Entre os pontos em evolução:

* Implementação de HTTPS (SSL/TLS)
* Proteção contra CSRF e XSS
* Fortalecimento do sistema de autenticação
* Melhor gerenciamento de sessões
* Validação rigorosa de uploads
* Logs e auditoria de atividades
* Controle de permissões (multiusuário)

> * ⚠️ A versão que se encontra disponível para download e uso está configurada para funcionar apenas em rede local.
> * Estou estudando sobre como levar ele para um ambiente externo de forma simples, segura e que qualquer pessoa possa configurar e fazer ela mesma.

---

### 🚧 Desafios Atuais

* Preparação para deploy em ambiente externo (VPS / cloud)
* Configuração de rede (DNS, domínio, acesso remoto)
* Automatização da instalação para usuários finais
* Otimização para múltiplos acessos simultâneos

---

### 🎯 Objetivo Final

Criar uma plataforma de armazenamento em nuvem que seja:

* 🔒 Segura por padrão
* ⚙️ Simples de instalar e usar
* 🌐 Acessível de qualquer lugar
* 🧠 Independente de serviços terceiros

---

## 🚧 Roadmap

* [ ] Upload com barra de progresso
* [ ] Drag & Drop
* [ ] Compartilhamento por link
* [ ] Sistema multiusuário
* [ ] Logs de atividade
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
