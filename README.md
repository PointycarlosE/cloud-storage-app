# 📁 Meu Drive Pessoal - Explorador de Arquivos Web

Um explorador de arquivos pessoal desenvolvido com Python/Flask, que permite navegar, visualizar e gerenciar arquivos diretamente no navegador. Uma alternativa self-hosted ao Google Drive para sua rede local.

![Tema Claro/Escuro](https://img.shields.io/badge/Tema-Claro%20%7C%20Escuro-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Funcionalidades

### 📂 Navegação
- Explorar pastas e arquivos do sistema
- Caminho de navegação interativo (breadcrumb)
- Botão para voltar à pasta anterior
- Suporte para arquivos de até 2GB

### 🎨 Interface
- **Tema claro/escuro** com botão de alternância (sem flash)
- **Visualização em grade ou lista** - escolha sua preferência
- **Design responsivo** - funciona em desktop, tablet e celular
- **Ícones dinâmicos** por tipo de arquivo (PDF, Word, Excel, imagens, etc.)

### 🔍 Busca e Organização
- **Pesquisa em tempo real** - filtra enquanto digita
- **Ordenação** por nome, tipo, tamanho ou data
- **Informações detalhadas** - tamanho formatado (KB, MB, GB) e data de modificação

### ✅ Seleção e Ações
- **Seleção múltipla** com checkboxes
- **Atalhos de teclado**: Ctrl+A para selecionar todos
- **Download individual** de arquivos
- **Upload de arquivos** para a pasta atual
- **Criar novas pastas**
- **Excluir** arquivos e pastas (com confirmação modal personalizada)

### 🖼️ Visualizadores
- **Lightbox para imagens** - navegação entre imagens com setas
- **Player de áudio** integrado nos cards
- **Visualização de PDF** em nova aba

### 🔒 Segurança
- Restrito à pasta base configurada (não permite sair)
- Validação de caminhos
- Nomes de arquivos sanitizados

## 🚀 Como instalar e executar

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/meu-drive-pessoal.git
cd meu-drive-pessoal
