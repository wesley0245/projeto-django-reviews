# Create your models here.

# central_reviews/models.py
from django.db import models
from django.contrib.auth.models import User # Para o 'autor'
from django.utils import timezone # Para a data de publicação

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorias" 
    def __str__(self):
        return self.nome

class Tenis(models.Model):
    nome = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    imagem_principal = models.ImageField(upload_to='tenis_imagens/', blank=True, null=True)
    # Relacionamento: Um tênis pertence a uma categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='tenis')

    def __str__(self):
        return f"{self.marca} {self.nome}"


class Review(models.Model):
    # Relacionamento: Um review pertence a um tênis
    tenis = models.ForeignKey(Tenis, on_delete=models.CASCADE, related_name='reviews')
    # Relacionamento: Um review pertence a um usuário (autor)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    titulo_review = models.CharField(max_length=200)
    texto_review = models.TextField()
    
    NOTA_CHOICES = [
        (1, '1 Estrela'),
        (2, '2 Estrelas'),
        (3, '3 Estrelas'),
        (4, '4 Estrelas'),
        (5, '5 Estrelas'),
    ]
    nota = models.IntegerField(choices=NOTA_CHOICES, default=5) 
    data_publicacao = models.DateTimeField(default=timezone.now)
    class Meta:
        # Ordena os reviews do mais novo para o mais antigo por padrão
        ordering = ['-data_publicacao'] 


    def __str__(self):
        return f"Review de {self.autor.username} para {self.tenis.nome}"



