from django.contrib import admin
from .models import Profile,TbUbsDadosSp,TbCalendarioVacina,TbMunicipios,TbParametros


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(TbCalendarioVacina)
class TbCalendarioVacinaAdmin(admin.ModelAdmin):
    list_display = ['id_vacina', 'cod_vacina', 'descricao_vacina','observacao','meses']
    search_fields = ('cod_vacina', 'descricao_vacina','observacao','meses')
    ordering = ['descricao_vacina']

@admin.register(TbMunicipios)
class TbMunicipios(admin.ModelAdmin):
    list_display = ['uf','município','região','população_2010']
    search_fields =('município',)
    ordering = ['uf', 'município', ]


@admin.register(TbParametros)
class TbParametrosAdmin(admin.ModelAdmin):
    list_display = ['parametro','valor','centraliza_latitude','centraliza_longitude']
    search_fields =('parametro',)
    ordering = ['parametro' ]


@admin.register(TbUbsDadosSp)
class TbUbsDadosSp(admin.ModelAdmin):
    list_display = ['codigoubs','codigonacionalsaude','endereçoubs','numeroenderecoubs',\
                    'cepubs','bairroenderecoubs','horariofuncionamentoubs','tipoprimeironivelubs',\
                    'tiposegundonivelubs','nometipoprimeironivel','telefone1ubs','telefone2ubs',\
                    'exibirreferenciaubs','informacoesidentificacaoubs','latitude','longitude']
    search_fields =('codigoubs',)
    ordering = [ '-codigoubs', ]
