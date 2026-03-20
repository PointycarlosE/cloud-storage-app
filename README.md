# 📁 Meu Drive Pessoal - Explorador de Arquivos Web

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

Um explorador de arquivos pessoal desenvolvido com Python/Flask, que permite navegar, visualizar e gerenciar arquivos diretamente no navegador. Uma alternativa self-hosted ao Google Drive para sua rede local.

![Screenshot](https://via.placeholder.com/800x400?text=Meu+Drive+Pessoal+Screenshot)

---

## ✨ Funcionalidades

### 🔐 Autenticação e Segurança
- **Sistema de login completo** com proteção contra força bruta (5 tentativas / 15 minutos)
- **Primeira execução intuitiva** - tela de criação de conta na primeira vez que o sistema roda
- **Senhas armazenadas com hash** (algoritmo scrypt/pbkdf2) - nunca armazenadas em texto plano
- **Sessões seguras** com cookies HttpOnly e SameSite
- **Variáveis de ambiente** para configurações sensíveis (.env fora do repositório)
- **Proteção de rotas** - redirecionamento automático para login

### 📂 Navegação
- Explorar pastas e arquivos do sistema
- Caminho de navegação interativo (breadcrumb)
- Botão para voltar à pasta anterior
- **Memória de posição** - ao voltar de uma pasta, mantém a rolagem onde você estava
- Suporte para arquivos de qualquer tamanho

### 🎨 Interface
- **Tema claro/escuro** com botão de alternância (sem flash branco)
- **Visualização em grade ou lista** - escolha sua preferência (persistente no localStorage)
- **Design totalmente responsivo** - funciona perfeitamente em desktop, tablet e celular
- **Ícones dinâmicos** por tipo de arquivo (PDF, Word, Excel, imagens, áudios, vídeos, código, etc.)
- **Toast notifications** elegantes para feedback de ações
- **Modal de confirmação personalizado** - substitui o alert() padrão

### 🔍 Busca e Organização
- **Pesquisa em tempo real** - filtra enquanto digita
- **Ordenação** por nome, tipo, tamanho ou data (com setas indicando direção)
- **Informações detalhadas**:
  - Tamanho formatado (B, KB, MB, GB)
  - Data de modificação inteligente ("Hoje às HH:MM", "Ontem às HH:MM", ou data completa)
  - Tipo do arquivo

### ✅ Seleção e Ações
- **Seleção múltipla** com checkboxes
- **Barra de ações** que aparece quando itens são selecionados
- **Atalhos de teclado**:
  - `Ctrl + A` - Selecionar todos os itens
  - `Delete` - Excluir itens selecionados
- **Download individual** de arquivos
- **Download em ZIP** - selecione múltiplos arquivos/pastas e baixe tudo em um arquivo compactado
- **Upload de múltiplos arquivos** - selecione vários arquivos de uma vez
- **Criar novas pastas**
- **Excluir** arquivos e pastas (individual ou múltiplo)

### 🖼️ Visualizadores
- **Lightbox para imagens** - navegação entre imagens com setas do teclado
- **Player de áudio** integrado nos cards
- **Visualização de PDF** em nova aba
- **Miniaturas** para imagens

### 🛡️ Segurança
- Restrito à pasta base configurada (não permite acesso fora dela)
- Validação de caminhos contra `../` (path traversal)
- Nomes de arquivos sanitizados com `secure_filename`
- Bloqueio de acesso a pastas sem permissão

---

## 🚀 Como instalar e executar

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/meu-drive-pessoal.git
cd meu-drive-pessoal

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt