# Generated by Django 3.2 on 2022-04-16 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0012_alter_driver_last_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='last_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='last_lng',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='drop_off_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='drop_off_lng',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pick_up_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pick_up_lng',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='taxi.driver'),
        ),
    ]
