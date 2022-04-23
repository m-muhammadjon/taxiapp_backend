# Generated by Django 3.2 on 2022-04-22 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0018_cancellationreason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancellation_reason',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='taxi.cancellationreason'),
        ),
    ]
