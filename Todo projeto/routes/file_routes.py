# routes/file_routes.py
import os
import shutil
import zipfile
import tempfile
from flask import render_template, abort, redirect, url_for, request, send_from_directory, send_file, Blueprint
from werkzeug.utils import secure_filename
from config import PASTA_BASE
from utils.helpers import get_info_arquivo

file_bp = Blueprint('file', __name__)

# -------- EXPLORADOR --------
@file_bp.route('/explorar/')
@file_bp.route('/explorar/<path:caminho>')
def explorar(caminho=""):
    try:
        # Monta caminho absoluto
        pasta_atual = os.path.abspath(os.path.join(PASTA_BASE, caminho))

        # Segurança: impedir sair da pasta base
        if os.path.commonpath([PASTA_BASE, pasta_atual]) != PASTA_BASE:
            abort(403)

        if not os.path.exists(pasta_atual):
            return render_template("erro.html", mensagem="Pasta não encontrada."), 404

        if not os.path.isdir(pasta_atual):
            return render_template("erro.html", mensagem="O caminho não é uma pasta."), 400

        itens = os.listdir(pasta_atual)

        pastas = []
        arquivos = []
        imagens = []
        audios = []

        exetensoes_imagens = ('.png','.jpg','.jpeg','.gif','.webp','.bmp')
        extensoes_audio = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')

        for item in itens:
            caminho_item = os.path.join(pasta_atual, item)
            item_info = get_info_arquivo(caminho_item, item)
            
            if os.path.isdir(caminho_item):
                item_info['tamanho_formatado'] = '--'
                pastas.append(item_info)
            else:
                nome_lower = item.lower()
                if nome_lower.endswith(exetensoes_imagens):
                    imagens.append(item_info)
                elif nome_lower.endswith(extensoes_audio):
                    audios.append(item_info)
                else:
                    arquivos.append(item_info)
                    
        # Pasta pai
        pasta_pai = os.path.dirname(caminho) if caminho else None

        # Breadcrumb
        partes = []
        if caminho:
            partes_caminho = caminho.split('/')
            caminho_acumulado = ""
            for parte in partes_caminho:
                if parte:
                    caminho_acumulado = parte if not caminho_acumulado else f"{caminho_acumulado}/{parte}"
                    partes.append({'nome': parte, 'caminho': caminho_acumulado})
                    
        return render_template(
            'explorar.html',
            pastas=pastas,
            arquivos=arquivos,
            imagens=imagens,
            audios=audios,
            caminho=caminho,
            caminho_atual=caminho,
            pasta_pai=pasta_pai,
            partes=partes
        )

    except PermissionError:
        return render_template("erro.html", mensagem="Acesso negado."), 403
    except Exception as e:
        return render_template("erro.html", mensagem=f"Erro inesperado: {str(e)}"), 500

# -------- DOWNLOAD INDIVIDUAL --------
@file_bp.route('/download/<path:caminho_arquivo>')
def download(caminho_arquivo):
    caminho_completo = os.path.abspath(os.path.join(PASTA_BASE, caminho_arquivo))

    if not caminho_completo.startswith(PASTA_BASE):
        abort(403)
    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        abort(404)

    pasta = os.path.dirname(caminho_completo)
    nome_arquivo = os.path.basename(caminho_completo)
    return send_from_directory(pasta, nome_arquivo, as_attachment=True)

# -------- VISUALIZAR ARQUIVO --------
@file_bp.route('/visualizar/<path:caminho_arquivo>')
def visualizar_arquivo(caminho_arquivo):
    caminho_completo = os.path.abspath(os.path.join(PASTA_BASE, caminho_arquivo))

    if os.path.commonpath([PASTA_BASE, caminho_completo]) != PASTA_BASE:
        abort(403)
    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        abort(404)

    pasta = os.path.dirname(caminho_completo)
    nome_arquivo = os.path.basename(caminho_completo)
    return send_from_directory(pasta, nome_arquivo, as_attachment=False)

# -------- UPLOAD DE ARQUIVOS --------
@file_bp.route('/upload/<path:caminho>', methods=['POST'])
@file_bp.route('/upload/', defaults={'caminho': ''}, methods=['POST'])
def upload(caminho):
    pasta_destino = os.path.abspath(os.path.join(PASTA_BASE, caminho))

    if os.path.commonpath([PASTA_BASE, pasta_destino]) != PASTA_BASE:
        abort(403)
    if not os.path.exists(pasta_destino) or not os.path.isdir(pasta_destino):
        abort(400)

    if 'arquivo' not in request.files:
        return "Nenhum arquivo enviado", 400

    arquivos = request.files.getlist('arquivo')
    
    if not arquivos or arquivos[0].filename == '':
        return "Nenhum arquivo válido", 400

    for arquivo in arquivos:
        if arquivo.filename == '':
            continue

        nome_seguro = secure_filename(arquivo.filename)
        caminho_final = os.path.join(pasta_destino, nome_seguro)

        contador = 1
        nome_base, extensao = os.path.splitext(nome_seguro)
        while os.path.exists(caminho_final):
            novo_nome = f"{nome_base}_{contador}{extensao}"
            caminho_final = os.path.join(pasta_destino, novo_nome)
            contador += 1

        arquivo.save(caminho_final)

    return redirect(url_for('file.explorar', caminho=caminho))

# -------- CRIAR PASTA --------
@file_bp.route('/criar_pasta/<path:caminho>', methods=['POST'])
@file_bp.route('/criar_pasta/', defaults={'caminho': ''}, methods=['POST'])
def criar_pasta(caminho):
    pasta_atual = os.path.abspath(os.path.join(PASTA_BASE, caminho))

    if os.path.commonpath([PASTA_BASE, pasta_atual]) != PASTA_BASE:
        abort(403)
    if not os.path.exists(pasta_atual) or not os.path.isdir(pasta_atual):
        abort(400)

    nome_pasta = request.form.get('nome_pasta')
    if not nome_pasta:
        return "Nome da pasta inválido", 400

    nome_seguro = secure_filename(nome_pasta)
    nova_pasta = os.path.join(pasta_atual, nome_seguro)

    try:
        os.mkdir(nova_pasta)
    except FileExistsError:
        return "A pasta já existe", 400
    except PermissionError:
        return "Sem permissão", 403

    return redirect(url_for('file.explorar', caminho=caminho))

# -------- DELETAR ARQUIVO --------
@file_bp.route('/deletar/<path:caminho_arquivo>', methods=['POST'])
def deletar_arquivo(caminho_arquivo):
    caminho_completo = os.path.abspath(os.path.join(PASTA_BASE, caminho_arquivo))

    if os.path.commonpath([PASTA_BASE, caminho_completo]) != PASTA_BASE:
        abort(403)
    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        return "Arquivo não encontrado", 404

    try:
        os.remove(caminho_completo)
    except PermissionError:
        return "Sem permissão", 403

    pasta_relativa = os.path.dirname(caminho_arquivo)
    return redirect(url_for('file.explorar', caminho=pasta_relativa))

# -------- DELETAR PASTA --------
@file_bp.route('/deletar_pasta/<path:caminho_pasta>', methods=['POST'])
def deletar_pasta(caminho_pasta):
    pasta_completa = os.path.abspath(os.path.join(PASTA_BASE, caminho_pasta))

    if os.path.commonpath([PASTA_BASE, pasta_completa]) != PASTA_BASE:
        abort(403)
    if not os.path.exists(pasta_completa) or not os.path.isdir(pasta_completa):
        return "Pasta não encontrada", 404

    try:
        shutil.rmtree(pasta_completa)
    except PermissionError:
        return "Sem permissão", 403

    pasta_pai = os.path.dirname(caminho_pasta)
    return redirect(url_for('file.explorar', caminho=pasta_pai))

# -------- DELETAR MÚLTIPLOS (AJAX) --------
@file_bp.route('/deletar_multiplos', methods=['POST'])
def deletar_multiplos():
    try:
        dados = request.get_json()
        caminhos = dados.get('caminhos', [])
        
        if not caminhos:
            return {'sucesso': False, 'erro': 'Nenhum item selecionado'}, 400
        
        erros = []
        sucessos = []
        
        for caminho_relativo in caminhos:
            caminho_completo = os.path.abspath(os.path.join(PASTA_BASE, caminho_relativo))
            
            if os.path.commonpath([PASTA_BASE, caminho_completo]) != PASTA_BASE:
                erros.append(f"{caminho_relativo}: Acesso negado")
                continue
            
            if not os.path.exists(caminho_completo):
                erros.append(f"{caminho_relativo}: Não encontrado")
                continue
            
            try:
                if os.path.isfile(caminho_completo):
                    os.remove(caminho_completo)
                    sucessos.append(caminho_relativo)
                elif os.path.isdir(caminho_completo):
                    shutil.rmtree(caminho_completo)
                    sucessos.append(caminho_relativo)
            except Exception as e:
                erros.append(f"{caminho_relativo}: {str(e)}")
        
        return {
            'sucesso': True,
            'sucessos': sucessos,
            'erros': erros,
            'total': len(caminhos),
            'excluidos': len(sucessos)
        }
    
    except Exception as e:
        return {'sucesso': False, 'erro': str(e)}, 500

# -------- DOWNLOAD EM ZIP --------
@file_bp.route('/download_zip', methods=['POST'])
def download_zip():
    temp_zip = None
    try:
        caminhos = request.form.getlist('caminhos')
        
        if not caminhos:
            return "Nenhum arquivo selecionado", 400
        
        temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        temp_zip.close()
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for caminho_relativo in caminhos:
                caminho_absoluto = os.path.abspath(os.path.join(PASTA_BASE, caminho_relativo))
                
                if os.path.commonpath([PASTA_BASE, caminho_absoluto]) != PASTA_BASE:
                    continue
                
                if os.path.exists(caminho_absoluto):
                    if os.path.isfile(caminho_absoluto):
                        zipf.write(caminho_absoluto, caminho_relativo)
                    elif os.path.isdir(caminho_absoluto):
                        for root, dirs, files in os.walk(caminho_absoluto):
                            for file in files:
                                file_path = os.path.join(root, file)
                                rel_path = os.path.relpath(file_path, PASTA_BASE)
                                zipf.write(file_path, rel_path)
        
        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name='arquivos_selecionados.zip',
            mimetype='application/zip'
        )
    
    except Exception as e:
        return f"Erro ao criar ZIP: {str(e)}", 500
    finally:
        if temp_zip and os.path.exists(temp_zip.name):
            try:
                os.unlink(temp_zip.name)
            except:
                pass