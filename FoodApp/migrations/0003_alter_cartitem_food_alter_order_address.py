# Generated by Django 5.0.2 on 2024-03-01 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0002_initial'),
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_items', to='FoodApp.fooditem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='UserApp.useraddress'),
        ),
    ]
