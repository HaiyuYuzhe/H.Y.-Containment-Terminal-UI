import requests
from bs4 import BeautifulSoup
import time
from django.core.management.base import BaseCommand
from arquivos_scp.models import Entidade

class Command(BaseCommand):
    help = 'Raspagem de dados limpa, ignorando rodapés e caixas de avaliação.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando varredura profunda..."))
        
        # Testando os SCPs que você abriu nas imagens
        for i in range(2, 175): 
            designacao = f"SCP-{i:03d}"
            url = f"http://scp-pt-br.wikidot.com/scp-{i:03d}"
            
            try:
                resposta = requests.get(url, timeout=10)
                if resposta.status_code != 200:
                    continue
                
                soup = BeautifulSoup(resposta.content, 'html.parser')
                conteudo = soup.find(id='page-content')
                if not conteudo:
                    continue
                
                # A CIRURGIA DE LIMPEZA: Procurar e destruir o lixo da Wiki
                classes_lixo = ['page-rate-widget-box', 'footer-wikiwalk-nav', 'licensebox', 'creditRate', 'info-container']
                for classe in classes_lixo:
                    elementos_lixo = conteudo.find_all('div', class_=classe)
                    for elemento in elementos_lixo:
                        elemento.decompose() # Apaga o elemento do HTML
                
                # Captura da imagem principal
                imagem_tag = conteudo.find('img')
                link_imagem = imagem_tag['src'] if imagem_tag else None
                
                # Extraindo o texto agora totalmente limpo
                texto_puro = conteudo.get_text(separator='\n').strip()
                
                # Regras de Classificação
                classe_encontrada = 'EUCLID'
                linhas = texto_puro.split('\n')
                for linha in linhas:
                    linha_upper = linha.upper()
                    if "CLASSE DO OBJETO:" in linha_upper or "CLASSE DE CONTENÇÃO:" in linha_upper:
                        if "SEGURO" in linha_upper or "SAFE" in linha_upper: classe_encontrada = 'SAFE'
                        elif "EUCLÍDEO" in linha_upper or "EUCLID" in linha_upper: classe_encontrada = 'EUCLID'
                        elif "KETER" in linha_upper: classe_encontrada = 'KETER'
                        elif "APOLLYON" in linha_upper: classe_encontrada = 'APOLLYON'
                
                Entidade.objects.update_or_create(
                    designacao=designacao,
                    defaults={
                        'nome_popular': f"Arquivo {designacao} [TRADUÇÃO]",
                        'classe': classe_encontrada,
                        'status': 'CONTIDO',
                        'imagem_url': link_imagem,
                        'procedimento_contencao': texto_puro, # Salvando o texto integral
                        'descricao': "Extração limpa via terminal PT-BR."
                    }
                )
                
                self.stdout.write(self.style.SUCCESS(f"[{designacao}] - Dados limpos salvos com sucesso."))
                time.sleep(1.5)
                
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Falha de conexão no {designacao}: {e}"))

        self.stdout.write(self.style.WARNING("Operação concluída."))