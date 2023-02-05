from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, TbCalendarioVacina, TbUbsDadosSp
from datetime import datetime
import pandas as pd
import pandas.tseries.offsets as ts
import folium
import requests
import json
import socket


def index(request):
    url = 'https://covid19-brazil-api.now.sh/api/report/v1'
    headers = {}
    response3 = requests.request('GET', url, data='data', headers=headers)
    dados_covid3 = json.loads(response3.content)
    df = pd.json_normalize(data=dados_covid3['data'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['datetime'] = pd.to_datetime(df['datetime']) - pd.DateOffset(hours=3)
    df['datetime'] = df['datetime'].dt.strftime('%d/%m/%Y %H:%M:%S')

    df_brasil = df[['cases', 'deaths', 'suspects', 'refuses']].sum().head()
    df_sao_paulo = df.query('uf=="SP"')
    df_sao_paulo = df_sao_paulo[['uf','cases', 'deaths', 'suspects', 'refuses', 'datetime']].sum().head()
    df_sao_paulo['cases'] = pd.to_numeric(df_sao_paulo['cases'], errors='ignore')

    df_data_atualizacao=df.query('uf=="SP"')
    df_data_atualizacao= df_data_atualizacao[['uf', 'datetime']].sum().head()


    return render(request, 'vacina/index.html', {'df_sao_paulo': df_sao_paulo, 'df_brasil': df_brasil,\
                                                 'df_data_atualizacao':df_data_atualizacao})


def vacinas_prazos(request):
    nova_data = request.GET.get('data_de_nascimento')
    if nova_data == None:
        nova_data = datetime.today()
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
        data_prevista=data_prevista + pd.offsets.BusinessDay()
        # incrementa o contador
        conta_mes = conta_mes + 1
        listadata += [data_prevista]

        # diasfalta += [dias]
    # adiciona a lista ao dataframe
    dados_sql['dataprevista'] = listadata
    if request.user.is_authenticated:
        print('ok')
    else:
        dados_sql = dados_sql.loc[(dados_sql['dataprevista'] >= datetime.today() - pd.DateOffset(days=1))]

    dados_sql.to_string(index=False)
    # transforma data para o formato brasileiro
    dados_sql['dataprevista'] = pd.to_datetime(dados_sql['dataprevista'])

    dados_sql['dataprevista'] = dados_sql['dataprevista'].dt.strftime('%d/%m/%Y')
    dados_sql2 = dados_sql.sort_values(by=['meses'], ascending=True)
    dados_sql3 = pd.DataFrame(dados_sql2)
    if request.user.is_authenticated:
        dados_sql3 = dados_sql3[['descricao_vacina', 'observacao','meses', 'dataprevista']]
    else:
       dados_sql3 = dados_sql3[['descricao_vacina', 'dataprevista']]
    dados_sql3.rename(
        columns={'descricao_vacina': 'Vacina', 'observacao': 'Observações',
                 'dataprevista': 'A partir de','meses':'Meses'},
        inplace=True
    )
    dados_sql3.to_string(index=False)
    context = {
        'vacin': 'Próximas Vacinas',
        'dados_sql3': dados_sql3.to_html(classes='table table-stripped', border=1, justify='center', index=False)
    }
    return render(request, 'vacina/vacinas_prazos.html', context)


def encontra_ubs(request):
    l1 = "-23.547169"
    l2 = "-46.636719"
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Local: {ip_address}")
    ip_address2 = "187.94.185.34"
    print(f"IP Address: {ip_address2}")
    ip = requests.get('https://api.ipify.org/')
    response = requests.post(f"http://ip-api.com/json/{ip_address}").json()
    print(response)
    if (response['status'] != 'fail'):
        l1 = response['lat']
        l2 = response['lon']
    ubs = TbUbsDadosSp.objects.all().values()
    geoloc_ubs = pd.DataFrame(ubs)
    # filtra o dataset com a variavel bairroubs
    geoloc = geoloc_ubs
    # seleciona a primeiralinha da pesquisa e utiliza a coordenada para centralizar o mapa
    # par ulilizar vinda do navegador  substitua geoloc.iloc[0]
    # geo_centraliza = geoloc.iloc[104]
    # print(geo_centraliza)
    # variaveis ppara a plotagem
    # mplotagem do mapa
    m = folium.Map(location=[l1, l2], zoom_start=14, control_scale=True, width=1090, height=450)
    folium.Marker(location=[float(l1), float(l2)]).add_to(m)
    for _, ubs in geoloc.iterrows():
        folium.Marker(
            location=[ubs['latitude'], ubs['longitude']], popup=ubs['endereçoubs']
        ).add_to(m)
    folium.Marker(
        location=[l1, l2], icon=folium.Icon(color='green', icon='home'), ).add_to(m)
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
