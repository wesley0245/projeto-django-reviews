# central_reviews/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CadastroView, TenisDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView # A view que você criou

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    
    # <int:pk> é um "coringa" do Django. Ele captura um número inteiro (o ID do tênis) da URL e o chama de 'pk' (Primary Key).
    path('tenis/<int:pk>/', TenisDetailView.as_view(), name='tenis-detail'),
    
    # Esta URL é "aninhada" dentro de um tênis específico
    # <int:tenis_pk> é o ID do tênis que estamos avaliando
    path('tenis/<int:tenis_pk>/review/novo/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/editar/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/deletar/', ReviewDeleteView.as_view(), name='review-delete'),
]
