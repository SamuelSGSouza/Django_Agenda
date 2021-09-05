from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat

def index(request):
    contatos = Contato.objects.order_by('id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 10)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, "contatos/index.html", {
        'contatos': contatos
    })

def ver_contato(request, id_contato):
    contato = get_object_or_404(Contato, id=id_contato)
    if not contato.mostrar:
        raise Http404
    return render(request, "contatos/ver_contato.html", {
        'contato': contato
    })

def busca(request):
    termo = request.GET.get('termo')
    campos = Concat('nome', Value(' '), 'sobrenome')
    if termo is None or not termo:
        raise Http404
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo),
        mostrar=True
    )
    paginator = Paginator(contatos, 10)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, "contatos/busca.html", {
        'contatos': contatos
    })