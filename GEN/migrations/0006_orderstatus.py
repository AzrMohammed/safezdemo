# Generated by Django 2.2.6 on 2020-11-27 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GEN', '0005_remove_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200, unique=True)),
                ('sub_text', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('status_note', models.CharField(max_length=200)),
                ('is_available', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(null=True)),
            ],
        ),
    ]