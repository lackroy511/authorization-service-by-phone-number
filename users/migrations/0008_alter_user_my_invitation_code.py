# Generated by Django 4.2.5 on 2023-10-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_invitation_code_user_my_invitation_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='my_invitation_code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True, verbose_name='мой код приглашения'),
        ),
    ]
