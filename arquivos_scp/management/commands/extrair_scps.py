import requests
from bs4 import BeautifulSoup
import time
from django.core.management.base import BaseCommand
from arquivos_scp.models import Entidade

class Command(BaseCommand):
    help = 'Executa a raspagem de dados massiva da Wiki SCP (Filial PT-BR) para o banco local.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Redirecionando proxy... Iniciando varredura nos servidores PT-BR..."))
        
        # Teste inicial do 2 ao 100
        for i in range(2, 9000):
            designacao = f"SCP-{i:03d}"
            # Alterado para a base de dados em português
            url = f"http://scp-pt-br.wikidot.com/scp-{i:03d}"
            
            try:
                resposta = requests.get(url, timeout=10)
                
                if resposta.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"[{designacao}] - Acesso negado, bloqueado ou inexistente."))
                    continue
                
                soup = BeautifulSoup(resposta.content, 'html.parser')
                conteudo = soup.find(id='page-content')
                
                if not conteudo:
                    continue
                
                texto_puro = conteudo.get_text(separator='\n')
                
                # Classe padrão caso o robô falhe em ler
                classe_encontrada = 'EUCLID'
                
                # Lógica de Localização: Lendo em português e traduzindo para a máquina
                linhas = texto_puro.split('\n')
                for linha in linhas:
                    linha_upper = linha.upper()
                    # A Wiki PT-BR costuma usar uma dessas duas nomenclaturas
                    if "CLASSE DO OBJETO:" in linha_upper or "CLASSE DE CONTENÇÃO:" in linha_upper:
                        if "SEGURO" in linha_upper: 
                            classe_encontrada = 'SAFE'
                        elif "EUCLÍDEO" in linha_upper or "EUCLIDEO" in linha_upper: 
                            classe_encontrada = 'EUCLID'
                        elif "KETER" in linha_upper: 
                            classe_encontrada = 'KETER'
                        elif "APOLLYON" in linha_upper or "APOLEÃO" in linha_upper: 
                            classe_encontrada = 'APOLLYON'
                
                # Salvando no banco
                Entidade.objects.update_or_create(
                    designacao=designacao,
                    defaults={
                        'nome_popular': f"Arquivo {designacao} [TRADUÇÃO]",
                        'classe': classe_encontrada,
                        'status': 'CONTIDO',
                        'procedimento_contencao': texto_puro[:1000] + "\n\n[ARQUIVO RESTANTE TRUNCADO NO TESTE...]",
                        'descricao': "Extração via terminal PT-BR."
                    }
                )
                
                self.stdout.write(self.style.SUCCESS(f"[{designacao}] - Dados lusófonos extraídos e contidos com sucesso."))
                
                # Furtividade: Pausa de 2 segundos. Sem isso, a Wikidot bloqueia o IP.
                time.sleep(2)
                
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Falha crítica de conexão no {designacao}: {e}"))

        self.stdout.write(self.style.WARNING("Varredura da filial PT-BR concluída."))