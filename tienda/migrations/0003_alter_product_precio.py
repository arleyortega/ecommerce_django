# Generated by Django 4.2.2 on 2023-12-09 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_product_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
