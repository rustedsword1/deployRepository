# Generated by Django 5.2.2 on 2025-06-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('reading', '読書中'), ('interested', '興味がある'), ('finished', '読了')], default='reading', max_length=20),
        ),
    ]
