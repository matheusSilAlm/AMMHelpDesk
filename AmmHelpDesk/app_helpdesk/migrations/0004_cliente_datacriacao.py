# Generated by Django 4.2.1 on 2023-06-04 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_helpdesk', '0003_alter_cliente_cpf_cnpj'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='datacriacao',
            field=models.DateTimeField(auto_now=True),
        ),
    ]