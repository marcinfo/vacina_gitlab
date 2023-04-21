import pandas as pd
from ninja import  NinjaAPI
from .models import  TbCalendarioVacina

import json
apis = NinjaAPI( title = 'API Vacina Paulistana' )
@apis.get('prazos/')
def listar(request):
    prazos = TbCalendarioVacina.objects.filter().order_by('-descricao_vacina').reverse()
    response = [{ 'monitor': i.descricao_vacina,\
                 'observacao': i.observacao,'meses': i.meses} for i in prazos]


    return response

@apis.get('vacinas/')
def listar(request):
    vacinas = TbCalendarioVacina.objects.values('descricao_vacina','observacao').order_by('descricao_vacina').distinct()
    vacinas_lista = list(vacinas)
    return vacinas_lista


