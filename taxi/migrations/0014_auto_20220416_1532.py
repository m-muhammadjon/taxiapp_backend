# Generated by Django 3.2 on 2022-04-16 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0013_auto_20220416_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drivers', to='taxi.cartype'),
        ),
    ]
