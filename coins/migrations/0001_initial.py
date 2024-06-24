# Generated by Django 4.0.1 on 2024-06-21 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteCoins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favourite Coin',
                'verbose_name_plural': 'Favourite Coins',
                'db_table': 'favourite_coins',
            },
        ),
        migrations.AddConstraint(
            model_name='favouritecoins',
            constraint=models.UniqueConstraint(fields=('user', 'coin_name'), name='unique_user_coin'),
        ),
    ]
