# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbCalendarioVacina(models.Model):
    id_vacina = models.AutoField(primary_key=True)
    cod_vacina = models.CharField(max_length=8)
    descricao_vacina = models.CharField(max_length=45)
    observacao = models.TextField()
    meses = models.IntegerField()
    status_vacina = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_calendario_vacina'


class TbLoginUsuario(models.Model):
    id_log_usuario = models.AutoField(primary_key=True)
    user_name_login = models.CharField(max_length=45)
    user_password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_usuario'


class TbMunicipioBrasil(models.Model):
    ibge7 = models.IntegerField(db_column='IBGE7', blank=True, null=True)  # Field name made lowercase.
    uf = models.TextField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    município = models.TextField(db_column='Município', blank=True, null=True)  # Field name made lowercase.
    região = models.TextField(db_column='Região', blank=True, null=True)  # Field name made lowercase.
    população_2010 = models.IntegerField(db_column='População 2010', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_municipiobrasil = models.AutoField(primary_key=True)

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


class TbParametros(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    parametro = models.CharField(max_length=45)
    valor = models.IntegerField()
    centraliza_latitude = models.FloatField(default=-23.55028,blank=True, null=True)
    centraliza_longitude = models.FloatField(default=-46.63389,max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_parametros'


class TbUbsBrasil(models.Model):
    cnes = models.TextField(db_column='CNES')  # Field name made lowercase.
    uf = models.IntegerField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    ibge = models.IntegerField(db_column='IBGE', blank=True, null=True)  # Field name made lowercase.
    nome = models.TextField(db_column='NOME', blank=True, null=True)  # Field name made lowercase.
    logradouro = models.TextField(db_column='LOGRADOURO', blank=True, null=True)  # Field name made lowercase.
    bairro = models.TextField(db_column='BAIRRO', blank=True, null=True)  # Field name made lowercase.
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    idubsbrasil = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_ubs_brasil'


class TbUbsDadosBrasil(models.Model):
    cnes = models.TextField(db_column='CNES')  # Field name made lowercase.
    uf = models.IntegerField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    ibge = models.IntegerField(db_column='IBGE', blank=True, null=True)  # Field name made lowercase.
    nome = models.TextField(db_column='NOME', blank=True, null=True)  # Field name made lowercase.
    logradouro = models.TextField(db_column='LOGRADOURO', blank=True, null=True)  # Field name made lowercase.
    bairro = models.TextField(db_column='BAIRRO', blank=True, null=True)  # Field name made lowercase.
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    idubsbrasil = models.AutoField(primary_key=True)

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


class VacinaProfile(models.Model):
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=100)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vacina_profile'
