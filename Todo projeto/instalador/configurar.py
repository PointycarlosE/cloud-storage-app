#!/usr/bin/env python3
# configurar.py - Script de configuração do Meu Drive Pessoal

import os
import sys
import shutil
import subprocess
import platform

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_colorido(texto, cor='verde'):
    """Imprime texto colorido"""
    cores = {
        'verde': '\033[92m',
        'amarelo': '\033[93m',
        'azul': '\033[94m',
        'vermelho': '\033[91m',
        'reset': '\033[0m'
    }
    if platform.system() == 'Windows':
        print(texto)
    else:
        print(f"{cores.get(cor, '')}{texto}{cores['reset']}")

def bem_vindo():
    """Tela de boas-vindas"""
    limpar_tela()
    print("=" * 60)
    print_colorido("📁 MEU DRIVE PESSOAL - INSTALADOR", 'azul')
    print("=" * 60)
    print()
    print("Este instalador vai configurar seu servidor de arquivos pessoal.")
    print()
    print_colorido("Recursos:", 'verde')
    print("  • Explorador de arquivos web")
    print("  • Upload/download de arquivos")
    print("  • Tema claro/escuro")
    print("  • Visualização de imagens")
    print("  • Player de áudio")
    print("  • Seleção múltipla")
    print("  • Download em ZIP")
    print()
    input("Pressione ENTER para continuar...")

def escolher_pasta_instalacao():
    """Pergunta onde instalar o projeto"""
    limpar_tela()
    print("=" * 60)
    print_colorido("📂 LOCAL DE INSTALAÇÃO", 'azul')
    print("=" * 60)
    print()
    
    if platform.system() == 'Windows':
        padrao = os.path.expanduser("~\\MeuDrivePessoal")
        print(f"Pasta padrão: {padrao}")
    else:
        padrao = os.path.expanduser("~/MeuDrivePessoal")
        print(f"Pasta padrão: {padrao}")
    
    print()
    escolha = input("Deseja usar a pasta padrão? (S/n): ").strip().lower()
    
    if escolha == 'n':
        print()
        caminho = input("Digite o caminho completo onde deseja instalar: ").strip()
        if not caminho:
            caminho = padrao
    else:
        caminho = padrao
    
    # Criar o diretório se não existir
    os.makedirs(caminho, exist_ok=True)
    
    return os.path.abspath(caminho)

def escolher_pasta_repositorio():
    """Pergunta qual pasta será o repositório de arquivos"""
    limpar_tela()
    print("=" * 60)
    print_colorido("📁 PASTA DO REPOSITÓRIO", 'azul')
    print("=" * 60)
    print()
    print("Esta será a pasta base que o servidor vai compartilhar.")
    print("Todos os arquivos e pastas dentro dela ficarão acessíveis.")
    print()
    
    if platform.system() == 'Windows':
        padrao = os.path.expanduser("~\\MeusArquivos")
        print(f"Pasta padrão: {padrao}")
    else:
        padrao = os.path.expanduser("~/MeusArquivos")
        print(f"Pasta padrão: {padrao}")
    
    print()
    escolha = input("Deseja usar a pasta padrão? (S/n): ").strip().lower()
    
    if escolha == 'n':
        print()
        caminho = input("Digite o caminho completo da pasta de repositório: ").strip()
        if not caminho:
            caminho = padrao
    else:
        caminho = padrao
    
    # Criar o diretório se não existir
    os.makedirs(caminho, exist_ok=True)
    
    return os.path.abspath(caminho)

def copiar_arquivos(origem, destino):
    """Copia os arquivos do projeto para o destino"""
    print_colorido("\n📋 Copiando arquivos...", 'amarelo')
    
    # Lista de arquivos/pastas para copiar
    itens = [
        'app.py', 'config.py', 'requirements.txt',
        'routes', 'utils', 'templates', 'static'
    ]
    
    for item in itens:
        origem_item = os.path.join(origem, item)
        destino_item = os.path.join(destino, item)
        
        if os.path.exists(origem_item):
            if os.path.isdir(origem_item):
                shutil.copytree(origem_item, destino_item, dirs_exist_ok=True)
                print(f"  📁 {item} -> OK")
            else:
                shutil.copy2(origem_item, destino_item)
                print(f"  📄 {item} -> OK")

def configurar_pasta_base(destino, pasta_repositorio):
    """Configura o PASTA_BASE no config.py"""
    config_path = os.path.join(destino, 'config.py')
    
    with open(config_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Substituir o caminho da pasta base
    novo_conteudo = conteudo.replace(
        'PASTA_BASE = os.path.abspath("C:/Users/cacae/REPOSITORIO")',
        f'PASTA_BASE = os.path.abspath(r"{pasta_repositorio}")'
    )
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)
    
    print_colorido(f"  ✅ Pasta base configurada: {pasta_repositorio}", 'verde')

def criar_ambiente_virtual(destino):
    """Cria e configura ambiente virtual"""
    print_colorido("\n🐍 Configurando ambiente virtual...", 'amarelo')
    
    venv_path = os.path.join(destino, 'venv')
    
    if platform.system() == 'Windows':
        python_cmd = 'python'
        venv_pip = os.path.join(venv_path, 'Scripts', 'pip')
        activate_cmd = os.path.join(venv_path, 'Scripts', 'activate')
    else:
        python_cmd = 'python3'
        venv_pip = os.path.join(venv_path, 'bin', 'pip')
        activate_cmd = os.path.join(venv_path, 'bin', 'activate')
    
    # Criar ambiente virtual
    subprocess.run([python_cmd, '-m', 'venv', venv_path], check=True)
    
    # Instalar dependências
    subprocess.run([venv_pip, 'install', '-r', os.path.join(destino, 'requirements.txt')], check=True)
    
    print_colorido(f"  ✅ Ambiente virtual criado", 'verde')
    return activate_cmd

def criar_atalho_inicializacao(destino):
    """Cria atalhos para iniciar o servidor"""
    print_colorido("\n🚀 Criando atalhos de inicialização...", 'amarelo')
    
    if platform.system() == 'Windows':
        # Criar arquivo .bat para Windows
        bat_path = os.path.join(destino, 'iniciar_servidor.bat')
        with open(bat_path, 'w') as f:
            f.write(f"""@echo off
cd /d {destino}
call venv\\Scripts\\activate
python app.py
pause
""")
        print(f"  📄 {bat_path} -> OK")
        
        # Criar atalho na área de trabalho (opcional)
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if os.path.exists(desktop):
            atalho = os.path.join(desktop, 'MeuDrivePessoal.url')
            with open(atalho, 'w') as f:
                f.write(f"""[InternetShortcut]
URL=http://localhost:5000
IconIndex=0
""")
            print(f"  📄 Atalho na área de trabalho -> OK")
    
    else:
        # Criar script .sh para Linux/Mac
        sh_path = os.path.join(destino, 'iniciar_servidor.sh')
        with open(sh_path, 'w') as f:
            f.write(f"""#!/bin/bash
cd {destino}
source venv/bin/activate
python3 app.py
""")
        os.chmod(sh_path, 0o755)
        print(f"  📄 {sh_path} -> OK")

def mensagem_final(destino):
    """Mostra mensagem de conclusão"""
    limpar_tela()
    print("=" * 60)
    print_colorido("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!", 'verde')
    print("=" * 60)
    print()
    print_colorido("📁 Projeto instalado em:", 'azul')
    print(f"   {destino}")
    print()
    print_colorido("🚀 Para iniciar o servidor:", 'azul')
    
    if platform.system() == 'Windows':
        print(f"   • Execute: {destino}\\iniciar_servidor.bat")
    else:
        print(f"   • Execute: {destino}/iniciar_servidor.sh")
    
    print()
    print_colorido("🌐 Para acessar:", 'azul')
    print("   • Local: http://localhost:5000")
    print("   • Rede: http://[IP_DO_SEU_PC]:5000")
    print()
    print_colorido("📁 Pasta do repositório:", 'azul')
    print("   • Configurei no config.py")
    print()
    print("=" * 60)
    input("Pressione ENTER para sair...")

def main():
    """Função principal"""
    # Pasta onde o instalador está rodando
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    bem_vindo()
    
    # Escolher pastas
    pasta_instalacao = escolher_pasta_instalacao()
    pasta_repositorio = escolher_pasta_repositorio()
    
    # Confirmar
    limpar_tela()
    print("=" * 60)
    print_colorido("📋 RESUMO DA INSTALAÇÃO", 'azul')
    print("=" * 60)
    print()
    print(f"Instalar em: {pasta_instalacao}")
    print(f"Repositório: {pasta_repositorio}")
    print()
    confirmar = input("Confirmar instalação? (S/n): ").strip().lower()
    
    if confirmar == 'n':
        print_colorido("\n❌ Instalação cancelada.", 'vermelho')
        sys.exit(0)
    
    # Executar instalação
    try:
        copiar_arquivos(pasta_atual, pasta_instalacao)
        configurar_pasta_base(pasta_instalacao, pasta_repositorio)
        criar_ambiente_virtual(pasta_instalacao)
        criar_atalho_inicializacao(pasta_instalacao)
        mensagem_final(pasta_instalacao)
        
    except Exception as e:
        print_colorido(f"\n❌ Erro durante a instalação: {e}", 'vermelho')
        sys.exit(1)

if __name__ == '__main__':
    main()