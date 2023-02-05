from ninja import  NinjaAPI
from .models import  TbCalendarioVacina,Vacinas

import json
apis = NinjaAPI( title = 'API Vacina Paulistana' )
@apis.get('prazos/')
def listar(request):
    prazos = TbCalendarioVacina.objects.all()
    response = [{ 'vacina': i.descricao_vacina,\
                 'observacao': i.observacao,'meses': i.meses} for i in prazos]
    print(response)

    return response

@apis.get('vacinas/')
def listar(request):
    prazos = TbCalendarioVacina.objects.all()
    response = [{ 'vacina': i.descricao_vacina,\
                 'observacao': i.observacao} for i in prazos]
    print(response)

    return response