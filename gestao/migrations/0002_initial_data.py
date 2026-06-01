from django.db import migrations


def create_initial_data(apps, schema_editor):
    TiposUtilizadores = apps.get_model('gestao', 'TiposUtilizadores')
    TiposPedido = apps.get_model('gestao', 'TiposPedido')

    usuarios = ['Administrador', 'Secretária', 'Rececionista', 'Técnico de Laboratório']
    pedidos = ['Exame Laboratorial', 'Raio-X', 'Ecografia', 'Eletrocardiograma']

    for nome in usuarios:
        TiposUtilizadores.objects.get_or_create(designacao=nome)

    for nome in pedidos:
        TiposPedido.objects.get_or_create(nome=nome)


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
