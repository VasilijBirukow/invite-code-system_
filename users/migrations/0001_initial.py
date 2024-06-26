# Generated by Django 5.0.4 on 2024-04-24 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=11)),
                ('applied_code', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applied_code', to='users.invitecode')),
                ('generated_code', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='generated_code', to='users.invitecode')),
            ],
        ),
    ]
