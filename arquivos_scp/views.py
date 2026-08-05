from django.shortcuts import render
from django.http import JsonResponse
from .models import Entidade

# Esta é a view que renderiza a interface visual que já fizemos
def painel_terminal(request):
    return render(request, 'terminal.html')

# Esta é a nova view da API (O Motor de Busca)
def buscar_entidade(request, designacao):
    try:
        # Busca no banco de dados o objeto exato. O '__iexact' faz com que
        # não importe se o usuário digitar "scp-002", "SCP-002" ou "Scp-002".
        anomalia = Entidade.objects.get(designacao__iexact=designacao)
        
        # Empacota os atributos do objeto em um dicionário Python
        dados = {
            'status': 'sucesso',
            'designacao': anomalia.designacao,
            'nome_popular': anomalia.nome_popular,
            'classe': anomalia.classe,
            'status_contencao': anomalia.status,
            'imagem_url': anomalia.imagem_url, # Hahaha Imagens agora
            'procedimentos': anomalia.procedimento_contencao,
            'descricao': anomalia.descricao
        }
        
        # Converte o dicionário em JSON e envia para o navegador
        return JsonResponse(dados)
        
    except Entidade.DoesNotExist:
        # Se a entidade não existir no banco, retorna um erro 404
        return JsonResponse({
            'status': 'erro', 
            'mensagem': 'REGISTRO NÃO ENCONTRADO. ACESSO NEGADO OU DADOS CORROMPIDOS.'
        }, status=404)