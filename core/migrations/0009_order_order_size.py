# Generated by Django 5.1.1 on 2025-02-03 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_size',
            field=models.CharField(default='M', max_length=3),
        ),
    ]
