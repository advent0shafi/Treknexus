# Generated by Django 4.2.2 on 2023-07-19 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userorder', '0003_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled'), ('DELIVERED', 'Delivered'), ('ORDERED', 'Ordered'), ('RETURNED', 'Returned'), ('SHIPPED', 'Shipped'), ('PROCESSING', 'Processing')], default='ordered', max_length=20),
        ),
    ]
