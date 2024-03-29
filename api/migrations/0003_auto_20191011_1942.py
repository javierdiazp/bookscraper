# Generated by Django 2.2.6 on 2019-10-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191010_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='product_description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='thumbnail_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='upc',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
