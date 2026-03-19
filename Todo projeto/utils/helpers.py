# utils/helpers.py
import os
import datetime

def formatar_tamanho(tamanho):
    """Formata tamanho de bytes para formato legível (KB, MB, GB, etc)"""
    if tamanho == '--' or tamanho == 0:
        return '--'
    
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            return f"{tamanho:.1f} {unidade}"
        tamanho /= 1024.0
    return f"{tamanho:.1f} PB"

def formatar_data(timestamp):
    """Formata timestamp para data legível (Hoje, Ontem, ou data específica)"""
    data_modificacao = datetime.datetime.fromtimestamp(timestamp)
    hoje = datetime.datetime.now().date()
    
    if data_modificacao.date() == hoje:
        return f"Hoje às {data_modificacao.strftime('%H:%M')}"
    elif data_modificacao.date() == (hoje - datetime.timedelta(days=1)):
        return f"Ontem às {data_modificacao.strftime('%H:%M')}"
    else:
        return data_modificacao.strftime('%d/%m/%Y %H:%M')

def get_info_arquivo(caminho_completo, nome):
    """Obtém informações de um arquivo/pasta"""
    stats = os.stat(caminho_completo)
    return {
        'nome': nome,
        'tamanho': stats.st_size,
        'tamanho_formatado': formatar_tamanho(stats.st_size),
        'data_modificacao': formatar_data(stats.st_mtime),
        'data_timestamp': stats.st_mtime
    }