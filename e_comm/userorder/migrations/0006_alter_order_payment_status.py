# Generated by Django 4.2.2 on 2023-07-19 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userorder', '0005_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled'), ('REFUNDED', 'Refunded')], default='ordered', max_length=20),
        ),
    ]
