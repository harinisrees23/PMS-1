# Generated by Django 3.2.9 on 2021-12-11 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_covid_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.customer'),
        ),
    ]
