# Generated by Django 2.2.1 on 2020-06-03 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0004_content_show_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='user_type',
            field=models.CharField(choices=[('stu', 'stu'), ('sup', 'sup')], default='stu', max_length=5),
        ),
    ]
