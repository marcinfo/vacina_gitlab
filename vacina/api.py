from ninja import  NinjaAPI
from .models import  TbCalendarioVacina

import json
apis = NinjaAPI( title = 'API Vacina Paulistana' )
@apis.get('prazos/')
def listar(request):
    prazos = TbCalendarioVacina.objects.all()
    response = [{ 'vacina': i.descricao_vacina,\
                 'observacao': i.observacao,'meses': i.meses} for i in prazos]
    print(response)

    return response

