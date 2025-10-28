
# Create your views here.



from django.views.generic import CreateView, ListView, DetailView

from django.views.generic.edit import UpdateView, DeleteView

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin # Para as mensagens

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q

from .models import Tenis, Review

from django.shortcuts import get_object_or_404


class CadastroView(SuccessMessageMixin, CreateView): 
    """
    Esta view (CBV) cuida da página de cadastro de novos usuários.
    """
    # Usa o formulário padrão de criação de usuário do Django
    form_class = UserCreationForm
    
    # O arquivo HTML que esta view vai mostrar
    template_name = 'registration/cadastro.html'
    
    # Para onde redirecionar o usuário após o cadastro dar certo
    success_url = reverse_lazy('login')
    
    # A mensagem que será mostrada após o cadastro (Requisito 'Mensagens')
    success_message = "Sua conta foi criada com sucesso! Faça o login."


class TenisListView(ListView):
    """
    Esta view (CBV) cuida da Homepage e lista todos os tênis.
    """
    model = Tenis # Diz ao Django para buscar objetos do modelo 'Tenis'
    
    # O arquivo HTML que esta view vai mostrar
    template_name = 'central_reviews/tenis_list.html' 
    
    # O nome da variável que poderemos usar no template
    # (em vez do padrão 'object_list')
    context_object_name = 'tenis_list'
    
    # --- REQUISITO OBRIGATÓRIO: Paginação ---
    paginate_by = 5 # Mostra 5 tênis por página


    # --- 2. ADICIONE ESTA FUNÇÃO ---
    def get_queryset(self):
        """
        Sobrescreve o queryset padrão para adicionar filtros de busca.
        """
        # Pega o queryset padrão (todos os tênis)
        queryset = super().get_queryset()
        
        # Pega o valor do parâmetro 'q' da URL (ex: /?q=busca)
        query = self.request.GET.get('q')
        
        if query:
            # Se 'q' tiver algum valor, filtra o queryset
            queryset = queryset.filter(
                Q(nome__icontains=query) | # OU
                Q(marca__icontains=query) 
            )
            # '__icontains' significa "contém, ignorando maiúsculas/minúsculas"
            
        return queryset
    
    # --- 3. (OPCIONAL) Envia o termo de busca de volta para o template ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Isso permite mostrar "Resultados para 'busca'"
        context['search_query'] = self.request.GET.get('q', '') 
        return context



class TenisDetailView(DetailView):
    """
    Esta view (CBV) mostra os detalhes de UM tênis específico
    e a lista de reviews associados a ele.
    """
    model = Tenis # Diz ao Django: "Busque UM objeto do modelo Tenis"
    
    # O arquivo HTML que esta view vai mostrar
    template_name = 'central_reviews/tenis_detail.html'
    
    # O nome da variável no template (em vez do padrão 'object')
    context_object_name = 'tenis'

    # Precisamos adicionar os REVIEWS ao contexto
    def get_context_data(self, **kwargs):
        # Pega o contexto padrão (que já tem o 'tenis')
        context = super().get_context_data(**kwargs)
        
        # Pega o objeto 'tenis' que esta view está mostrando
        tenis = self.get_object() 
        
        # Busca todos os reviews relacionados a este tênis
        # e os adiciona ao contexto
        context['reviews_list'] = Review.objects.filter(tenis=tenis)
        
        return context
    


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Esta view (CBV) cuida do formulário para ADICIONAR um novo review.
    'LoginRequiredMixin' bloqueia usuários não logados.
    """
    model = Review # O modelo que queremos criar
    
    # O arquivo HTML que esta view vai mostrar
    template_name = 'central_reviews/review_form.html'
    
    # Os campos que o usuário poderá preencher
    fields = ['titulo_review', 'texto_review', 'nota']

    # Esta função é chamada QUANDO o formulário é válido (antes de salvar)
    def form_valid(self, form):
        # Pega o 'tenis' baseado no 'pk' (ID) que está na URL
        # (ex: 'tenis/1/review/novo/')
        form.instance.tenis = get_object_or_404(Tenis, pk=self.kwargs['tenis_pk'])
        
        # Pega o 'autor' automaticamente do usuário que está logado
        form.instance.autor = self.request.user
        
        # Agora sim, salva o formulário com o tênis e o autor definidos
        return super().form_valid(form)

    # Para onde redirecionar o usuário após o review ser criado
    def get_success_url(self):
        # Redireciona de volta para a página de detalhes do tênis
        # que ele acabou de avaliar
        return reverse_lazy('tenis-detail', kwargs={'pk': self.kwargs['tenis_pk']})



class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Esta view (CBV) cuida de EDITAR um review existente.
    'LoginRequiredMixin' bloqueia usuários não logados.
    'UserPassesTestMixin' bloqueia quem não for o autor.
    """
    model = Review
    
    # Usa o MESMO template do formulário de criação
    template_name = 'central_reviews/review_form.html'
    
    # Os campos que o usuário pode editar
    fields = ['titulo_review', 'texto_review', 'nota']
    
    # Esta função é o teste para o 'UserPassesTestMixin'
    def test_func(self):
        # Pega o review que o usuário está tentando editar
        review = self.get_object()
        
        # Verifica se o usuário logado (request.user) é o MESMO
        # que o autor do review (review.autor)
        return self.request.user == review.autor

    # Para onde redirecionar após a edição
    def get_success_url(self):
        # Redireciona de volta para a página de detalhes do tênis
        review = self.get_object()
        return reverse_lazy('tenis-detail', kwargs={'pk': review.tenis.pk})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Esta view (CBV) cuida de DELETAR um review existente.
    """
    model = Review
    
    # Template para a página de confirmação "Você tem certeza?"
    template_name = 'central_reviews/review_confirm_delete.html'
    
    # O nome da variável no template (em vez do padrão 'object')
    context_object_name = 'review'
    
    # O mesmo teste: só o autor pode deletar
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.autor

    # Para onde redirecionar após deletar
    def get_success_url(self):
        review = self.get_object()
        return reverse_lazy('tenis-detail', kwargs={'pk': review.tenis.pk})