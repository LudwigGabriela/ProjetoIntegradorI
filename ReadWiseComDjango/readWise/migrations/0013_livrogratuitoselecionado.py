# Generated by Django 5.2.3 on 2025-06-20 01:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("readWise", "0012_promocao"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LivroGratuitoSelecionado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("genero", models.CharField(max_length=100)),
                ("mes", models.DateField(auto_now_add=True)),
                (
                    "ebook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="readWise.ebook"
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
