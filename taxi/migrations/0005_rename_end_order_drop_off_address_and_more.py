# Generated by Django 4.0.3 on 2022-04-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0004_remove_order_trip_time_driver_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='end',
            new_name='drop_off_address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='start',
            new_name='pick_up_address',
        ),
        migrations.AddField(
            model_name='order',
            name='arrived',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='ended',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='penalty_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='started',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('in_progress', 'In_progess'), ('started', 'Started'), ('ended', 'Ended'), ('cancelled', 'Cancelled')], default='requested', max_length=20),
        ),
    ]