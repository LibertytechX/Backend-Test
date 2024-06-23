from django.db import models

from core.models import User

# Create your models here.


class FavouriteCoins(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    coin_name = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favourite_coins'
        verbose_name = "Favourite Coin"
        verbose_name_plural = "Favourite Coins"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "coin_name"], name="unique_user_coin"
            )
        ]
