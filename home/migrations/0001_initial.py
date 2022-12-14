# Generated by Django 3.2.3 on 2022-12-12 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Company_Name', models.CharField(max_length=250)),
                ('Company_Tagline', models.CharField(max_length=250)),
                ('Address', models.CharField(max_length=250)),
                ('State', models.CharField(max_length=250)),
                ('City', models.CharField(max_length=250)),
                ('Pin_code', models.IntegerField()),
                ('Email', models.EmailField(max_length=254, null=True)),
                ('Partner', models.CharField(max_length=250, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_email', models.EmailField(max_length=254)),
                ('job_position', models.CharField(max_length=250)),
                ('is_hr', models.BooleanField(blank=True, null=True)),
                ('is_manager', models.BooleanField(blank=True, null=True)),
                ('hiring_date', models.DateField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeavesRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Duration_From', models.DateTimeField(default=django.utils.timezone.now)),
                ('Duration_To', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Approved'), ('3', 'Rejected')], default='Pending', max_length=500)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.employees')),
            ],
        ),
    ]