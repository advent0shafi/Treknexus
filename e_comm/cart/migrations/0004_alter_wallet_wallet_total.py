# Generated by Django 4.2.2 on 2023-07-15 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
