# Generated by Django 4.0.2 on 2022-12-13 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channel_entries', to='channel.channel')),
            ],
        ),
        migrations.CreateModel(
            name='FieldEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=10, max_digits=20)),
                ('channel_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_entries', to='channel.channelentry')),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_entries', to='channel.field')),
            ],
        ),
    ]
