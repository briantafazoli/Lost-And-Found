# Generated by Django 5.0.3 on 2024-04-19 18:11

import django.db.models.deletion
import django.utils.timezone
import items.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('status', models.PositiveIntegerField(choices=[(100, 'New'), (200, 'Flagged'), (300, 'In Progress'), (400, 'Resolved')], default=100)),
                ('tag', models.PositiveIntegerField(choices=[(1, 'Other'), (100, 'Air Pods'), (300, 'Rain Jacket'), (301, 'Umbrella'), (302, 'Sunglasses')])),
                ('date', models.DateField(default=django.utils.timezone.now, validators=[items.models.date_validator])),
                ('expiration_date', models.DateField(default=items.models.return_expiration_date)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=50, null=True, validators=[items.models.PhoneNumberValidator()])),
                ('resolve_text', models.CharField(blank=True, default=None, max_length=1024, null=True)),
                ('is_found', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.location')),
            ],
        ),
        migrations.CreateModel(
            name='ItemFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='imageUpload/')),
                ('type', models.CharField(max_length=30)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
        ),
    ]
