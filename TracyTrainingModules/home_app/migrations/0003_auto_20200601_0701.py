# Generated by Django 2.2.1 on 2020-06-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0002_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='user_type',
            field=models.CharField(choices=[('Student', 'stu'), ('Supervisor', 'sup')], default='stu', max_length=5),
        ),
    ]