# Generated by Django 5.2.2 on 2025-06-11 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('reading', '読書中'), ('interested', '興味がある'), ('finished', '読了')], default='interested', max_length=20),
        ),
    ]
