# Generated by Django 4.0.3 on 2022-04-09 06:20

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0003_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='trip_time',
        ),
        migrations.AddField(
            model_name='driver',
            name='location',
            field=location_field.models.plain.PlainLocationField(max_length=63, null=True),
        ),
    ]
