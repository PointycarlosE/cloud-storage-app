Aqui está o README.md completo e organizado para você copiar e colar:

# 📁 Meu Drive Pessoal - Explorador de Arquivos Web

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

Um explorador de arquivos pessoal desenvolvido com Python/Flask, que permite navegar, visualizar e gerenciar arquivos diretamente no navegador. Uma alternativa self-hosted ao Google Drive para sua rede local.

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
    -  obs: individual ainda em produção

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

# 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/meu-drive-pessoal.git
cd meu-drive-pessoal
```
# 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
```
# 3. Ative o ambiente virtual

## Windows:
```bash
venv\Scripts\activate
```
## Linux/Mac:
```bash
source venv/bin/activate
```

# 4. Instale as dependências
```bash
pip install -r requirements.txt
```
---
### Primeira Execução

1. **Inicie o servidor:**
```bash
python app.py
```

2. **Acesse no navegador:**
```
http://localhost:5000
```

3. **Configure sua conta:**
   - Na primeira execução, você será redirecionado para a tela de criação de conta
   - Digite seu nome de usuário e senha (mínimo 6 caracteres)
   - Defina a pasta que será usada como repositório de arquivos
   - Exemplo: `C:\Users\SeuUsuario\MeuDriveRepositorio` (Windows) ou `/home/usuario/MeuDriveRepositorio` (Linux)

4. **Reinicie o servidor** (Ctrl+C e `python app.py` novamente)
    - Necessário para a criação dos arquivos de configuração
    - Pretendo arrumar isso para não ser necessário reiniciar

5. **Faça login** com as credenciais criadas

### Acesso na Rede Local

Para acessar de outros dispositivos na mesma rede:

1. Descubra o IP do seu computador:
   ```bash
   # Windows:
   ipconfig
   # Linux/Mac:
   ifconfig
   ```

2. Acesse de outro dispositivo:
   ```
   http://[IP_DO_SEU_COMPUTADOR]:5000
   ```

> ⚠️ **Importante**: Certifique-se de que o firewall não esteja bloqueando a porta 5000.

---

## 🛠️ Estrutura do Projeto

```
meu-drive-pessoal/
├── app.py                 # Aplicação principal
├── config.py              # Configurações centrais
├── .env                   # Variáveis de ambiente (criado na primeira execução)
├── requirements.txt       # Dependências
├── auth/                  # Módulo de autenticação
│   ├── __init__.py
│   ├── models.py          # Modelo de usuário
│   ├── routes.py          # Rotas de login/logout/setup
│   └── decorators.py      # Decoradores de proteção de rotas
├── routes/                # Rotas da aplicação
│   ├── __init__.py
│   ├── main_routes.py     # Rotas principais (home, objetivos)
│   └── file_routes.py     # Rotas de arquivos (explorar, upload, download)
├── utils/                 # Utilitários
│   ├── __init__.py
│   └── helpers.py         # Funções auxiliares (formatação, etc.)
├── templates/             # Templates HTML
│   ├── home.html
│   ├── objetivos.html
│   ├── explorar.html
│   ├── login.html
│   ├── setup.html
│   └── erro.html
└── static/                # Arquivos estáticos
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── main.js        # Scripts globais (tema, toast, modal)
    │   └── explorar.js    # Scripts do explorador
    └── img/
        └── favicon.ico
```

---

## 🔧 Configuração Avançada

### Alterar a Pasta Base

Edite o arquivo `.env` gerado na primeira execução:

```bash
PASTA_BASE=C:\Users\SeuUsuario\NovaPasta
```

### Alterar a Porta

No `config.py`:

```python
PORT = 8080  # ou qualquer outra porta
```

### Desabilitar o Login (para desenvolvimento)

No `config.py`:

```python
REQUIRE_LOGIN = False
```

### Gerar Nova Chave Secreta

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copie o resultado e substitua `SECRET_KEY` no arquivo `.env`.

---

## 📦 Dependências

```txt
Flask==2.3.3
Werkzeug==2.3.7
Flask-Login==0.6.2
python-dotenv==1.0.0
```

---

## 🚧 Em Desenvolvimento

### Instalador Automático (em breve)

Estou desenvolvendo instaladores automáticos para Windows e Linux que vão:

- Baixar o projeto do GitHub
- Configurar o ambiente virtual automaticamente
- Criar o arquivo `.env` com suas credenciais
- Criar atalhos na área de trabalho
- Iniciar o servidor automaticamente

> ⚠️ **Status**: Em desenvolvimento. Por enquanto, siga as instruções manuais acima.

---

## 🎯 Próximas Funcionalidades

- [ ] **Instalador automático** (Windows/Linux)
- [ ] **Barra de progresso para uploads**
- [ ] **Arrastar e soltar** para upload
- [ ] **Favoritos / Pastas rápidas**
- [ ] **Histórico de navegação** (botões voltar/avançar)
- [ ] **Visualização de vídeos**
- [ ] **Modo offline com Service Worker**
- [ ] **Compartilhamento de arquivos com links temporários**
- [ ] **Múltiplos usuários** com permissões
- [ ] **Log de atividades**

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@PointycarlosE](https://github.com/PointycarlosE)


---

## 🙏 Agradecimentos

- Inspirado no Google Drive e Windows Explorer
- Comunidade Flask pela excelente documentação
- Todos os contribuidores que ajudaram no projeto

---

**Desenvolvido com ❤️ para uso pessoal e aprendizado**
---
⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!
