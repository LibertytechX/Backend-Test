# Create a management command to fetch coin data
# api/management/commands/fetch_coin_data.py
import requests
from django.core.management.base import BaseCommand

from core.models import Coin


class Command(BaseCommand):
    help = "Fetch coin data from CoinAPI"

    def handle(self, *args, **kwargs):
        api_key = "5EDE76A4-29E0-4E5B-8505-FEEFED9B29B3"
        url = "https://rest.coinapi.io/v1/assets"
        headers = {"X-CoinAPI-Key": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            print(data)
            # Access the rates key in the response
            for coin_data in data[:100]:
                Coin.objects.update_or_create(
                    name=coin_data["asset_id"],
                    defaults={
                        "usd_price": coin_data.get("price_usd", 0),
                        "volume": coin_data.get("volume_1mth_usd", 0),
                    },
                )
            self.stdout.write(self.style.SUCCESS("Successfully fetched coin data"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching data from CoinAPI: {e}"))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f"Key error: {e}"))
