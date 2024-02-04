# Generated by Django 4.2.7 on 2023-12-04 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_token_profile_phone_friend_profile_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friend_profile', to='accounts.profile', verbose_name='user'),
        ),
    ]
