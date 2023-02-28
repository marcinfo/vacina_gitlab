import pandas as pd
import folium
import pytz
import requests
import json
from folium.plugins import MarkerCluster
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, TbCalendarioVacina, TbUbsDadosSp,TbParametros
from datetime import datetime
from geopy import distance

from geopy.geocoders import Nominatim



def index(request):
    url = 'https://covid19-brazil-api.now.sh/api/report/v1'
    vacina_covid = 'https://www.saopaulo.sp.gov.br/wp-content/uploads/2023/02/20230228_vacinometro.csv'
    leitos_publico = 'https://www.saopaulo.sp.gov.br/wp-content/uploads/2023/02/20230228_leitos_ocupados_por_unidade_hospitalar.zip'
    # casos_covid = 'https://www.saopaulo.sp.gov.br/wp-content/uploads/2023/02/20230210_dados_covid_municipios_sp.csv'
    vacina_covid_sp = pd.read_csv(vacina_covid, sep=';')
    vacina_covid_sp = vacina_covid_sp.loc[vacina_covid_sp['MUNICÍPIO'] != 'Grand Total']
    # casos_covid_sp = pd.read_csv(casos_covid, sep=';')
    leitos_ocupados_sp = pd.read_csv(leitos_publico, sep=';')

    leitos_ocupados_sp.rename(
        columns={'Leitos Ocupados / Enfermaria': 'enfermaria', 'Leitos Ocupados / UTI': 'uti'},
        inplace=True
    )
    leitos_ocupados_sp = leitos_ocupados_sp[['enfermaria', 'uti']].sum().head()

    vacina_covid_sp.rename(
        columns={'1° DOSE': 'dose1', '2° DOSE': 'dose2', '3° DOSE': 'dose3', \
                 'REFORCO': 'reforco', '2 REFORCO': 'reforco2', '3 REFORCO': 'reforco3', \
                 'ADICIONAL': 'adicional', 'Grand Total': 'total'},
        inplace=True
    )
    vacina_covid_sp1 = vacina_covid_sp[['UNICA', 'dose1', 'dose2', 'adicional']]

    vacina_covid_sp1 = vacina_covid_sp.sum()

    headers = {}
    response3 = requests.request('GET', url, data='data', headers=headers)
    dados_covid3 = json.loads(response3.content)
    df = pd.json_normalize(data=dados_covid3['data'])
    df = df.sort_values(by='cases', ascending=False)
    df = df.rename(columns={'state': 'estado', 'cases': 'casos', 'deaths': 'mortes', 'suspects': 'suspeitos' \
        , 'refuses': 'nao_confirmados', 'datetime': 'atualizacao'})
    df = df.reset_index()
    df['atualizacao'] = pd.to_datetime(df['atualizacao'])
    df['atualizacao'] = pd.to_datetime(df['atualizacao']) - pd.DateOffset(hours=3)
    df['atualizacao'] = df['atualizacao'].dt.strftime('%d/%m/%Y %H:%M:%S')
    df = df[['uf', 'estado', 'casos', 'mortes', 'suspeitos', 'nao_confirmados', 'atualizacao']]

    df_brasil = df[['casos', 'mortes', 'suspeitos', 'nao_confirmados']].sum().head()
    df_sao_paulo = df.query('uf=="SP"')
    df_sao_paulo = df_sao_paulo[['uf', 'casos', 'mortes', 'suspeitos', 'nao_confirmados', 'atualizacao']].sum().head()
    df_sao_paulo['casos'] = pd.to_numeric(df_sao_paulo['casos'], errors='ignore')

    df_data_atualizacao = datetime.now(pytz.timezone('America/Sao_Paulo'))

    return render(request, 'vacina/index.html', {'df_sao_paulo': df_sao_paulo, 'df_brasil': df_brasil, \
                                                 'df_data_atualizacao': df_data_atualizacao,
                                                 'leitos_ocupados_sp': leitos_ocupados_sp, \
                                                 'vacina_covid_sp1': vacina_covid_sp1,
                                                 'atualizacao': df_data_atualizacao})


def vacinas_prazos(request):
    nova_data = request.GET.get('data_de_nascimento')

    if nova_data == None:
        nova_data = datetime.today()
    data_selecionada = nova_data
    ##transfoma a dataa para o formato intenacional
    vac = TbCalendarioVacina.objects.all().values()
    dados_sql = pd.DataFrame(vac)
    dados_sql.index_col = False
    # Contador para o for
    conta_mes = 0
    # lista vazia que vai receber os valores de (data + meses)
    listadata = []
    diasfalta = []
    # percorre todas as linhas da tabela
    for (row, rs) in dados_sql.iterrows():
        # recebe a quntidade de mes e coloca na quantidade_mes
        quantidade_mes = int(dados_sql['meses'].values[conta_mes])
        # adiciona a quaantidade de mêses na data
        # data_prevista = nova_data + relativedelta(months = quantidade_mes)
        data_prevista = pd.to_datetime(nova_data) + pd.DateOffset(months=quantidade_mes)
        data_prevista = ((data_prevista - pd.DateOffset(days=1)) + pd.offsets.BusinessDay())
        # incrementa o contador
        conta_mes = conta_mes + 1
        listadata += [data_prevista]

        # diasfalta += [dias]
    # adiciona a lista ao dataframe
    dados_sql['dataprevista'] = listadata

    if request.user.is_authenticated:
        print('ok')
    else:
        dados_sql = dados_sql.loc[(dados_sql['dataprevista'] >= datetime.today() + pd.DateOffset(days=7))]

    dados_sql.to_string(index=False)
    # transforma data para o formato brasileiro
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])

    dados_sql['dataprevista'] = dados_sql['dataprevista'].dt.strftime('%d/%m/%Y')
    dados_sql2 = dados_sql.sort_values(by=['meses'], ascending=True)
    dados_sql3 = pd.DataFrame(dados_sql2)
    if request.user.is_authenticated:
        dados_sql3 = dados_sql3[['descricao_vacina', 'observacao', 'meses', 'dataprevista']]
    else:
        dados_sql3 = dados_sql3[['descricao_vacina', 'dataprevista']]
    dados_sql3.rename(
        columns={'descricao_vacina': 'Vacina', 'observacao': 'Observações',
                 'dataprevista': 'A partir de', 'meses': 'Meses'},
        inplace=True
    )
    dados_sql3.to_string(index=False)
    df_data_atualizacao = datetime.now(pytz.timezone('America/Sao_Paulo'))
    context = {
        'nova_data': df_data_atualizacao,
        'vacin': 'Próximas Vacinas',
        'dados_sql3': dados_sql3.to_html(classes='table table-stripped', border=1, justify='center', index=False)
    }

    return render(request, 'vacina/vacinas_prazos.html', context)
def encontra_ubs(request):
    lat_get = request.GET.get('lat')
    lon_get = request.GET.get('lon')
    status = 'Iniciando o Processamento, Aguarde!'

    if (lat_get == None) & (lon_get == None):
        return render(request, 'vacina/encontra_ubs.html')
        #geoloc = geoloc_ubs
    else:
        url = 'https://sage.saude.gov.br/paineis/ubsFuncionamento/lista.php?output=csv'



        param = TbParametros.objects.all().values()
        param = pd.DataFrame(param)
        parametro = param.groupby('parametro').sum().reset_index()

        zoom_localizacao = parametro.query('parametro=="zoom_localizacao"')
        zoom_localizacao = float(zoom_localizacao['valor'])

        qtd_ubs_localizacao = parametro.query('parametro=="qtd_ubs_localizacao"')
        qtd_ubs_localizacao = int(qtd_ubs_localizacao['valor'])
        usb_sp = pd.read_csv(url, sep=";")
        usb_sp2 = usb_sp.dropna(axis=0)
        geoloc_ubs_sp = pd.DataFrame(usb_sp2)
        latitude = str(lat_get)
        longitude = str(lon_get)
        l1 = latitude
        l2 = longitude
        zoom = zoom_localizacao
        quantidade = qtd_ubs_localizacao
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(l1 + "," + l2)
        address = location.raw['address']
        cidade = address.get('city')
        estado= address.get('ISO3166-2-lvl4')[3:5]
        geoloc_ubs_sp = geoloc_ubs_sp.loc[(geoloc_ubs_sp["uf"] == estado) & (geoloc_ubs_sp["cidade"] == cidade)]

    lista_distancia=[]
    for _, dis in geoloc_ubs_sp.iterrows():
        distan = distance.distance((l1, l2), [float(dis['lat']), dis['long']]).km
        distan = float(distan)
        distan = round(distan,1)
        lista_distancia += [distan]
    geoloc_ubs_sp['distancia'] = lista_distancia
    geoloc_ubs_sp = geoloc_ubs_sp[['cidade','no_logradouro','no_bairro','lat','long','distancia']]
    geoloc_ubs_sp = geoloc_ubs_sp.nsmallest(quantidade, 'distancia')
    geoloc_ubs_sp['poupup']= 'DISTANCIA '+geoloc_ubs_sp['distancia'].map(str)+' km ' +\
                             geoloc_ubs_sp['no_logradouro']+' '+geoloc_ubs_sp['no_bairro']
    m = folium.Map(location=[l1, l2], zoom_start=zoom, control_scale=True, width=1090, height=450)
    folium.Marker(location=[float(l1), float(l2)]).add_to(m)
    for _, ubs in geoloc_ubs_sp.iterrows():
        folium.Marker(
            location=[ubs['lat'], ubs['long']], popup=ubs['poupup'],
        ).add_to(m)
    folium.Marker(
        location=[l1, l2], popup='Você esta aqui!', icon=folium.Icon(color='green', icon='ok-circle'), ).add_to(m)
    context = {
        'vacin': 'Encontre a UBS mais proxima de você.',
        'm': m._repr_html_()
    }
    return render(request, 'vacina/encontra_ubs.html', context)
def minhas_vacinas(request):
    nascimento = request.user.profile.date_of_birth
    ##transfoma a dataa para o formato intenacional
    vac = TbCalendarioVacina.objects.all().values()
    dados_sql = pd.DataFrame(vac)
    dados_sql.index_col = False
    # Contador para o for
    conta_mes = 0
    # lista vazia que vai receber os valores de (data + meses)
    listadata = []
    diasfalta = []
    # percorre todas as linhas da tabela
    for (row, rs) in dados_sql.iterrows():
        # recebe a quntidade de mes e coloca na quantidade_mes
        quantidade_mes = int(dados_sql['meses'].values[conta_mes])
        # adiciona a quaantidade de mêses na data
        # data_prevista = nova_data + relativedelta(months = quantidade_mes)
        data_prevista = pd.to_datetime(nascimento) + pd.DateOffset(months=quantidade_mes)
        data_prevista = data_prevista + pd.offsets.BusinessDay()
        # incrementa o contador
        conta_mes = conta_mes + 1
        listadata += [data_prevista]
        # diasfalta += [dias]
    # adiciona a lista ao dataframe
    dados_sql['dataprevista'] = listadata
    dados_sql.to_string(index=False)
    # transforma data para o formato brasileiro
    # dados_sql = dados_sql.loc[(dados_sql['dataprevista'] >= datetime.today())]
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])
    dados_sql['dataprevista'] = dados_sql['dataprevista'].dt.strftime('%d/%m/%Y')
    dados_sql2 = dados_sql.sort_values(by=['meses'], ascending=True)
    dados_sql3 = pd.DataFrame(dados_sql2)
    dados_sql3 = dados_sql3[['descricao_vacina', 'observacao', 'meses', 'dataprevista', 'status_vacina']]
    dados_sql3.rename(
        columns={'descricao_vacina': 'Vacina', 'observacao': 'Observções', 'meses': 'Meses',
                 'dataprevista': 'A partir de', 'status_vacina': 'Status da Vacina'},
        inplace=True)
    dados_sql3.to_string(index=False)
    context = {
        'vacin': 'Minhas Vacinas',
        'dados_sql3': dados_sql3.to_html(classes='table table-stripped', border=1, justify='center', index=False)
    }
    return render(request, 'vacina/minhas_vacinas.html', context)
def links(request):
    return render(request, 'vacina/links.html')
def api(request):
    return render(request, 'vacina/api.html')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'vacina/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'vacina/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'vacina/register.html',
                  {'user_form': user_form})
@login_required
def dashboard(request):
    return render(request, 'vacina/dashboard.html', {'section': 'dashboard'})
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Atualizado com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'vacina/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
