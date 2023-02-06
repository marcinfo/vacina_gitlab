from django.db import models
from django.conf import settings
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=False, null=False)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name='Foto')
    def __str__(self):
        return f'Profile for user {self.user.username}'

class TbCalendarioVacina(models.Model):
    id_vacina = models.AutoField(primary_key=True)
    cod_vacina = models.CharField(max_length=8)
    descricao_vacina = models.CharField(max_length=45)
    observacao = models.CharField(max_length=45)
    meses = models.IntegerField()
    status_vacina = models.CharField(max_length=45, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tb_calendario_vacina'
        verbose_name = "Tabela de vacina"
        verbose_name_plural = "Cadastro de Vacinas"


class TbLoginUsuario(models.Model):
    id_log_usuario = models.AutoField(primary_key=True)
    user_name_login = models.CharField(max_length=45)
    user_password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_usuario'


class TbMunicipioBrasil(models.Model):
    id_municipiobrasil = models.AutoField(primary_key=True)
    ibge7 = models.IntegerField(db_column='IBGE7', blank=True, null=True)  # Field name made lowercase.
    uf = models.TextField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    município = models.TextField(db_column='Município', blank=True, null=True)  # Field name made lowercase.
    região = models.TextField(db_column='Região', blank=True, null=True)  # Field name made lowercase.
    população_2010 = models.IntegerField(db_column='População 2010', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'tb_municipio_brasil'


class TbMunicipios(models.Model):
    ibge7 = models.IntegerField(db_column='IBGE7', blank=True, null=True)  # Field name made lowercase.
    uf = models.TextField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    município = models.TextField(db_column='Município', blank=True, null=True)  # Field name made lowercase.
    região = models.TextField(db_column='Região', blank=True, null=True)  # Field name made lowercase.
    população_2010 = models.IntegerField(db_column='População 2010', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'tb_municipios'
        verbose_name = "Tabela de municipio"
        verbose_name_plural = "Cadastro de Municipios"

class TbUbsDadosBrasil(models.Model):
    cnes = models.TextField(db_column='CNES')  # Field name made lowercase.
    uf = models.IntegerField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    ibge = models.IntegerField(db_column='IBGE', blank=True, null=True)  # Field name made lowercase.
    nome = models.TextField(db_column='NOME', blank=True, null=True)  # Field name made lowercase.
    logradouro = models.TextField(db_column='LOGRADOURO', blank=True, null=True)  # Field name made lowercase.
    bairro = models.TextField(db_column='BAIRRO', blank=True, null=True)  # Field name made lowercase.
    latitude = models.TextField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.TextField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_ubs_dados_brasil'


class TbUbsDadosSp(models.Model):
    codigoubs = models.IntegerField(db_column='codigoUBS')  # Field name made lowercase.
    codigonacionalsaude = models.IntegerField(db_column='codigoNacionalSaude')  # Field name made lowercase.
    endereçoubs = models.TextField(db_column='endereçoUBS')  # Field name made lowercase.
    numeroenderecoubs = models.CharField(db_column='numeroEnderecoUBS', max_length=10)  # Field name made lowercase.
    cepubs = models.CharField(db_column='cepUBS', max_length=10)  # Field name made lowercase.
    bairroenderecoubs = models.CharField(db_column='bairroEnderecoUBS', max_length=45)  # Field name made lowercase.
    horariofuncionamentoubs = models.CharField(db_column='horarioFuncionamentoUBS', max_length=45)  # Field name made lowercase.
    tipoprimeironivelubs = models.CharField(db_column='tipoPrimeiroNivelUBS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tiposegundonivelubs = models.CharField(db_column='tipoSegundoNivelUBS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nometipoprimeironivel = models.CharField(db_column='nomeTipoPrimeiroNivel', max_length=45, blank=True, null=True)  # Field name made lowercase.
    telefone1ubs = models.CharField(db_column='telefone1UBS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    telefone2ubs = models.CharField(db_column='telefone2UBS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    exibirreferenciaubs = models.CharField(db_column='exibirReferenciaUBS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    informacoesidentificacaoubs = models.TextField(db_column='informacoesIdentificacaoUBS', blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    idubsbrasil_field = models.AutoField(db_column="idubsbrasil'", primary_key=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'tb_ubs_dados_sp'
        verbose_name = "Tabela de UBS"
        verbose_name_plural = "Cadastro de UBS"
