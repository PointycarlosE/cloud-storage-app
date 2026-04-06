# app/routes/files.py
import os
import shutil
import zipfile
import tempfile
from flask import (
    render_template, abort, redirect, url_for,
    request, send_from_directory, send_file, Blueprint, current_app
)
from werkzeug.utils import secure_filename
from flask_login import current_user

from app.config import PASTA_BASE, MAX_ZIP_FILES, MAX_ZIP_SIZE_MB
from app.utils.helpers import get_info_arquivo
from app.auth.decorators import login_required_optional
from app.utils.audit import (
    log_upload, log_upload_bloqueado, log_download,
    log_delete, log_acesso_negado, log_path_traversal, log_zip_bloqueado
)

file_bp = Blueprint('file', __name__)


# ===== HELPER: VALIDAÇÃO DE CAMINHO =====
def caminho_seguro(caminho_relativo: str) -> str | None:
    """
    Resolve o caminho relativo dentro de PASTA_BASE.
    Retorna o caminho absoluto se for seguro, None se for path traversal.
    Usa commonpath (consistente em todo o código).
    """
    try:
        caminho_abs = os.path.abspath(os.path.join(PASTA_BASE, caminho_relativo))
        pasta_base_abs = os.path.abspath(PASTA_BASE)
        # commonpath levanta ValueError se os paths estiverem em drives diferentes (Windows)
        if os.path.commonpath([pasta_base_abs, caminho_abs]) != pasta_base_abs:
            return None
        return caminho_abs
    except (ValueError, TypeError):
        return None


# ===== EXTENSÕES BLOQUEADAS NO UPLOAD =====
# Arquivos executáveis e de script não devem ser enviados
EXTENSOES_BLOQUEADAS = {
    '.php', '.php3', '.php4', '.php5', '.phtml',  # PHP
    '.sh', '.bash', '.zsh', '.fish',               # Shell
    '.py', '.pyc', '.pyw',                         # Python
    '.rb', '.pl', '.cgi',                          # Ruby / Perl / CGI
    '.exe', '.bat', '.cmd', '.com',                # Windows executáveis
    '.js', '.mjs',                                 # JavaScript server-side
    '.jar', '.class',                              # Java
    '.htaccess', '.htpasswd',                      # Configurações de servidor
}


def extensao_bloqueada(nome_arquivo: str) -> bool:
    _, ext = os.path.splitext(nome_arquivo.lower())
    return ext in EXTENSOES_BLOQUEADAS


# ===== EXPLORADOR =====
@file_bp.route('/explorar/')
@file_bp.route('/explorar/<path:caminho>')
@login_required_optional
def explorar(caminho=""):
    try:
        pasta_atual = caminho_seguro(caminho)

        if pasta_atual is None:
            log_path_traversal(caminho)
            abort(403)

        if not os.path.exists(pasta_atual):
            return render_template("erro.html", mensagem="Pasta não encontrada."), 404

        if not os.path.isdir(pasta_atual):
            return render_template("erro.html", mensagem="O caminho não é uma pasta."), 400

        itens = os.listdir(pasta_atual)
        pastas, arquivos, imagens, audios = [], [], [], []

        extensoes_imagens = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        extensoes_audio = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')

        for item in itens:
            caminho_item = os.path.join(pasta_atual, item)
            item_info = get_info_arquivo(caminho_item, item)

            if os.path.isdir(caminho_item):
                item_info['tamanho_formatado'] = '--'
                pastas.append(item_info)
            else:
                nome_lower = item.lower()
                if nome_lower.endswith(extensoes_imagens):
                    imagens.append(item_info)
                elif nome_lower.endswith(extensoes_audio):
                    audios.append(item_info)
                else:
                    arquivos.append(item_info)

        pasta_pai = os.path.dirname(caminho) if caminho else None

        partes = []
        if caminho:
            caminho_acumulado = ""
            for parte in caminho.split('/'):
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
    except Exception:
        return render_template("erro.html", mensagem="Erro inesperado."), 500


# ===== LISTA PARCIAL (AJAX) =====
@file_bp.route('/partial/lista/<path:caminho>')
@file_bp.route('/partial/lista/', defaults={'caminho': ''})
@login_required_optional
def lista_parcial(caminho=""):
    pasta_atual = caminho_seguro(caminho)

    if pasta_atual is None:
        log_path_traversal(caminho)
        abort(403)

    if not os.path.exists(pasta_atual) or not os.path.isdir(pasta_atual):
        abort(404)

    itens = os.listdir(pasta_atual)
    pastas, arquivos, imagens, audios = [], [], [], []

    extensoes_imagens = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
    extensoes_audio = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')

    for item in itens:
        caminho_item = os.path.join(pasta_atual, item)
        item_info = get_info_arquivo(caminho_item, item)

        if os.path.isdir(caminho_item):
            item_info['tamanho_formatado'] = '--'
            pastas.append(item_info)
        else:
            nome_lower = item.lower()
            if nome_lower.endswith(extensoes_imagens):
                imagens.append(item_info)
            elif nome_lower.endswith(extensoes_audio):
                audios.append(item_info)
            else:
                arquivos.append(item_info)

    return render_template(
        'partials/_lista_arquivos.html',
        pastas=pastas,
        arquivos=arquivos,
        imagens=imagens,
        audios=audios,
        caminho=caminho
    )


# ===== DOWNLOAD INDIVIDUAL =====
@file_bp.route('/download/<path:caminho_arquivo>')
@login_required_optional
def download(caminho_arquivo):
    caminho_completo = caminho_seguro(caminho_arquivo)

    if caminho_completo is None:
        log_path_traversal(caminho_arquivo)
        abort(403)

    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        abort(404)

    log_download(current_user.username, caminho_arquivo)
    pasta = os.path.dirname(caminho_completo)
    nome_arquivo = os.path.basename(caminho_completo)
    return send_from_directory(pasta, nome_arquivo, as_attachment=True)


# ===== VISUALIZAR ARQUIVO =====
@file_bp.route('/visualizar/<path:caminho_arquivo>')
@login_required_optional
def visualizar_arquivo(caminho_arquivo):
    caminho_completo = caminho_seguro(caminho_arquivo)

    if caminho_completo is None:
        log_path_traversal(caminho_arquivo)
        abort(403)

    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        abort(404)

    pasta = os.path.dirname(caminho_completo)
    nome_arquivo = os.path.basename(caminho_completo)
    return send_from_directory(pasta, nome_arquivo, as_attachment=False)


# ===== UPLOAD =====
@file_bp.route('/upload/<path:caminho>', methods=['POST'])
@file_bp.route('/upload/', defaults={'caminho': ''}, methods=['POST'])
@login_required_optional
def upload(caminho):
    pasta_destino = caminho_seguro(caminho)

    if pasta_destino is None:
        log_path_traversal(caminho)
        abort(403)

    if not os.path.exists(pasta_destino) or not os.path.isdir(pasta_destino):
        abort(400)

    if 'arquivo' not in request.files:
        return "Nenhum arquivo enviado", 400

    arquivos = request.files.getlist('arquivo')
    if not arquivos or arquivos[0].filename == '':
        return "Nenhum arquivo válido", 400

    usuario = current_user.username

    for arquivo in arquivos:
        if arquivo.filename == '':
            continue

        nome_seguro = secure_filename(arquivo.filename)

        if not nome_seguro:
            log_upload_bloqueado(usuario, arquivo.filename, 'nome inválido após sanitização')
            continue

        if extensao_bloqueada(nome_seguro):
            log_upload_bloqueado(usuario, nome_seguro, 'extensão bloqueada')
            return f"Tipo de arquivo não permitido: {os.path.splitext(nome_seguro)[1]}", 400

        caminho_final = os.path.join(pasta_destino, nome_seguro)

        # Evitar sobrescrever arquivos existentes
        contador = 1
        nome_base, extensao = os.path.splitext(nome_seguro)
        while os.path.exists(caminho_final):
            novo_nome = f"{nome_base}_{contador}{extensao}"
            caminho_final = os.path.join(pasta_destino, novo_nome)
            contador += 1

        arquivo.save(caminho_final)
        log_upload(usuario, caminho, os.path.basename(caminho_final))

    return redirect(url_for('file.explorar', caminho=caminho))


# ===== CRIAR PASTA =====
@file_bp.route('/criar_pasta/<path:caminho>', methods=['POST'])
@file_bp.route('/criar_pasta/', defaults={'caminho': ''}, methods=['POST'])
@login_required_optional
def criar_pasta(caminho):
    pasta_atual = caminho_seguro(caminho)

    if pasta_atual is None:
        log_path_traversal(caminho)
        abort(403)

    if not os.path.exists(pasta_atual) or not os.path.isdir(pasta_atual):
        abort(400)

    nome_pasta = request.form.get('nome_pasta', '').strip()
    if not nome_pasta:
        return "Nome da pasta inválido", 400

    nome_seguro = secure_filename(nome_pasta)
    if not nome_seguro:
        return "Nome da pasta inválido após sanitização", 400

    nova_pasta = os.path.join(pasta_atual, nome_seguro)

    # Verificar que a nova pasta ainda está dentro da base
    if caminho_seguro(os.path.relpath(nova_pasta, PASTA_BASE)) is None:
        abort(403)

    try:
        os.mkdir(nova_pasta)
    except FileExistsError:
        return "A pasta já existe", 400
    except PermissionError:
        return "Sem permissão", 403

    return redirect(url_for('file.explorar', caminho=caminho))


# ===== DELETAR ARQUIVO =====
@file_bp.route('/deletar/<path:caminho_arquivo>', methods=['POST'])
@login_required_optional
def deletar_arquivo(caminho_arquivo):
    caminho_completo = caminho_seguro(caminho_arquivo)

    if caminho_completo is None:
        log_path_traversal(caminho_arquivo)
        abort(403)

    if not os.path.exists(caminho_completo) or not os.path.isfile(caminho_completo):
        return "Arquivo não encontrado", 404

    try:
        os.remove(caminho_completo)
        log_delete(current_user.username, caminho_arquivo)
    except PermissionError:
        return "Sem permissão", 403

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return {'sucesso': True, 'mensagem': 'Arquivo excluído com sucesso'}

    pasta_relativa = os.path.dirname(caminho_arquivo)
    return redirect(url_for('file.explorar', caminho=pasta_relativa))


# ===== DELETAR PASTA =====
@file_bp.route('/deletar_pasta/<path:caminho_pasta>', methods=['POST'])
@login_required_optional
def deletar_pasta(caminho_pasta):
    pasta_completa = caminho_seguro(caminho_pasta)

    if pasta_completa is None:
        log_path_traversal(caminho_pasta)
        abort(403)

    if not os.path.exists(pasta_completa) or not os.path.isdir(pasta_completa):
        return "Pasta não encontrada", 404

    try:
        shutil.rmtree(pasta_completa)
        log_delete(current_user.username, caminho_pasta)
    except PermissionError:
        return "Sem permissão", 403

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return {'sucesso': True, 'mensagem': 'Pasta excluída com sucesso'}

    pasta_pai = os.path.dirname(caminho_pasta)
    return redirect(url_for('file.explorar', caminho=pasta_pai))


# ===== DELETAR MÚLTIPLOS (AJAX) =====
@file_bp.route('/deletar_multiplos', methods=['POST'])
@login_required_optional
def deletar_multiplos():
    try:
        dados = request.get_json()
        if not dados:
            return {'sucesso': False, 'erro': 'Dados inválidos'}, 400

        caminhos = dados.get('caminhos', [])

        # Limite de itens por requisição
        if not caminhos:
            return {'sucesso': False, 'erro': 'Nenhum item selecionado'}, 400
        if len(caminhos) > 500:
            return {'sucesso': False, 'erro': 'Máximo de 500 itens por operação'}, 400

        erros, sucessos = [], []
        usuario = current_user.username

        for caminho_relativo in caminhos:
            if not isinstance(caminho_relativo, str):
                continue

            caminho_completo = caminho_seguro(caminho_relativo)

            if caminho_completo is None:
                log_path_traversal(caminho_relativo)
                erros.append(f"{caminho_relativo}: Acesso negado")
                continue

            if not os.path.exists(caminho_completo):
                erros.append(f"{caminho_relativo}: Não encontrado")
                continue

            try:
                if os.path.isfile(caminho_completo):
                    os.remove(caminho_completo)
                elif os.path.isdir(caminho_completo):
                    shutil.rmtree(caminho_completo)
                log_delete(usuario, caminho_relativo)
                sucessos.append(caminho_relativo)
            except Exception as ex:
                erros.append(f"{caminho_relativo}: {str(ex)}")

        return {
            'sucesso': True,
            'sucessos': sucessos,
            'erros': erros,
            'total': len(caminhos),
            'excluidos': len(sucessos)
        }

    except Exception:
        return {'sucesso': False, 'erro': 'Erro interno'}, 500


# ===== DOWNLOAD EM ZIP =====
@file_bp.route('/download_zip', methods=['POST'])
@login_required_optional
def download_zip():
    usuario = current_user.username
    caminhos = request.form.getlist('caminhos')

    if not caminhos:
        return "Nenhum arquivo selecionado", 400

    # Limite de quantidade de arquivos no ZIP
    if len(caminhos) > MAX_ZIP_FILES:
        log_zip_bloqueado(usuario, f"muitos arquivos: {len(caminhos)} > {MAX_ZIP_FILES}")
        return f"Máximo de {MAX_ZIP_FILES} itens por ZIP", 400

    temp_zip = None
    try:
        temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        temp_zip.close()

        tamanho_total = 0
        max_bytes = MAX_ZIP_SIZE_MB * 1024 * 1024

        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for caminho_relativo in caminhos:
                if not isinstance(caminho_relativo, str):
                    continue

                caminho_absoluto = caminho_seguro(caminho_relativo)
                if caminho_absoluto is None:
                    log_path_traversal(caminho_relativo)
                    continue

                if not os.path.exists(caminho_absoluto):
                    continue

                if os.path.isfile(caminho_absoluto):
                    tamanho_total += os.path.getsize(caminho_absoluto)
                    if tamanho_total > max_bytes:
                        log_zip_bloqueado(usuario, f"tamanho excedido: >{MAX_ZIP_SIZE_MB}MB")
                        return f"Seleção excede o limite de {MAX_ZIP_SIZE_MB}MB por ZIP", 400
                    zipf.write(caminho_absoluto, caminho_relativo)

                elif os.path.isdir(caminho_absoluto):
                    for root, dirs, files in os.walk(caminho_absoluto):
                        for file in files:
                            file_path = os.path.join(root, file)
                            tamanho_total += os.path.getsize(file_path)
                            if tamanho_total > max_bytes:
                                log_zip_bloqueado(usuario, f"tamanho excedido: >{MAX_ZIP_SIZE_MB}MB")
                                return f"Seleção excede o limite de {MAX_ZIP_SIZE_MB}MB por ZIP", 400
                            rel_path = os.path.relpath(file_path, PASTA_BASE)
                            zipf.write(file_path, rel_path)

        log_download(usuario, f"[ZIP] {len(caminhos)} itens")

        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name='arquivos_selecionados.zip',
            mimetype='application/zip'
        )

    except Exception:
        return "Erro ao criar ZIP", 500
    finally:
        # Tentar deletar o arquivo temporário após o envio
        if temp_zip and os.path.exists(temp_zip.name):
            try:
                os.unlink(temp_zip.name)
            except OSError:
                pass