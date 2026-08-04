from django.db import models

class Entidade(models.Model):
    # Níveis de classificação inspirados no universo de contenção
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

    designacao = models.CharField(max_length=100, verbose_name="Designação (Ex: Item-001)")
    nome_popular = models.CharField(max_length=150, verbose_name="Nome de Registro")
    classe = models.CharField(max_length=20, choices=CLASSES_CONTENCAO, default='EUCLID')
    status = models.CharField(max_length=20, choices=STATUS_ATUAL, default='CONTIDO')
    
    # Textos longos para você escrever a sua narrativa
    procedimento_contencao = models.TextField(verbose_name="Procedimentos Especiais de Contenção")
    descricao = models.TextField(verbose_name="Descrição da Anomalia")
    
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.designacao} - {self.nome_popular}"