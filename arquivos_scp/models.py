from django.db import models

class Entidade(models.Model):
    CLASSES_CONTENCAO = [
        ('SAFE', 'Safe - Contenção Estável'),
        ('EUCLID', 'Euclid - Comportamento Imprevisível'),
        ('KETER', 'Keter - Ameaça de Fuga Ativa'),
        ('APOLLYON', 'Apollyon - Impossível de Conter'),
    ]

    STATUS_ATUAL = [
        ('CONTIDO', 'Contido com Sucesso'),
        ('BRECHA', 'Alerta de Brecha Crítica'),
        ('DESCONHECIDO', 'Paradeiro Desconhecido'),
    ]

    designacao = models.CharField(max_length=100, verbose_name="Designação")
    nome_popular = models.CharField(max_length=150, verbose_name="Nome de Registro")
    classe = models.CharField(max_length=20, choices=CLASSES_CONTENCAO, default='EUCLID')
    status = models.CharField(max_length=20, choices=STATUS_ATUAL, default='CONTIDO')
    
    # NOVA GAVETA: Para armazenar o link da imagem da anomalia
    imagem_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name="URL da Imagem de Contenção")
    
    procedimento_contencao = models.TextField(verbose_name="Procedimentos Especiais")
    descricao = models.TextField(verbose_name="Descrição da Anomalia")
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.designacao} - {self.nome_popular}"