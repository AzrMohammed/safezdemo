# Generated by Django 2.2.6 on 2020-12-04 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GEN', '0025_brandbasicinfo_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GEN.BrandBasicInfo'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='brand_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GEN.BrandBranchBasicInfo'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='servisable_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GEN.BranchServisableProduct'),
        ),
    ]
