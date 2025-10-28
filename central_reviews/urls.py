# central_reviews/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CadastroView, TenisDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView # A view que você criou

urlpatterns = [
    # URL de Login: Usa a CBV pronta do Django
    # Ela vai procurar automaticamente o template 'registration/login.html'
    path('login/', LoginView.as_view(), name='login'),
    
    # URL de Logout: Usa a CBV pronta
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # URL de Cadastro: Usa a sua 'CadastroView'
    path('cadastro/', CadastroView.as_view(), name='cadastro'),

    # --- 2. ADICIONE A URL DE DETALHE ---
    # <int:pk> é um "coringa" do Django. Ele captura um número 
    # inteiro (o ID do tênis) da URL e o chama de 'pk' (Primary Key).
    path('tenis/<int:pk>/', TenisDetailView.as_view(), name='tenis-detail'),

    # --- 2. ADICIONE A URL DE CRIAR REVIEW ---
    # Esta URL é "aninhada" dentro de um tênis específico
    # <int:tenis_pk> é o ID do tênis que estamos avaliando
    path('tenis/<int:tenis_pk>/review/novo/', ReviewCreateView.as_view(), name='review-create'),

    # --- 2. ADICIONE AS URLs DE UPDATE E DELETE ---
    # Estas URLs usam o ID (pk) do REVIEW
    
    path('review/<int:pk>/editar/', ReviewUpdateView.as_view(), name='review-update'),


    path('review/<int:pk>/deletar/', ReviewDeleteView.as_view(), name='review-delete'),
]
