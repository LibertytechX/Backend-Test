"""
    This file is to define functions or code snippets to be used once or multiple times,
    within the program, allowing other files focus on logic intended 
    whilst using pieces of code necessary for the program from here.
"""

import requests
import environ
import aiohttp
import asyncio

from rest_framework.pagination import PageNumberPagination

env = environ.Env()
environ.Env.read_env()


def currency_formatter(number):
    """
    Formats the float amount, return the understandable format also as float.
    """
    if type(number) is str:
        return
    curr = float(number)
    currency = f"{curr:,}"
    return currency   
   

class CoinAPI:
    COIN_API_BASE_URL = "https://api.coinapi.io"
    headers = {
        "Accept": "text/plain",
        "X-CoinAPI-Key": env("COIN_API_KEY")
    }

    @staticmethod
    def _handle_response(response):
        """
        Helper method to handle API responses
        """
        if response.status_code == 200:
            return response.json()
        else:
            return response

    @staticmethod
    def fetch_coin_by_id(coin_id: str):
        """
        Calls the coin API, requesting for coin with the specified ID
        """
        url = f"{CoinAPI.COIN_API_BASE_URL}/v1/assets/{coin_id}"
       
        response = requests.get(url, headers=CoinAPI.headers)
        return CoinAPI._handle_response(response)

    @staticmethod
    def fetch_all_coins():
        """
        Calls the coin API, requesting for all coins
        """
        url = f"{CoinAPI.COIN_API_BASE_URL}/v1/assets"

        response = requests.get(url, headers=CoinAPI.headers)
        return CoinAPI._handle_response(response)

    @staticmethod
    async def fetch_multiple_coin_by_id(coin_id_list: list):
        """
        To call the coin API asynchronously and simultaneously fetch coins the list of coin id passed
        """
        coins_list = []
        actions = []
        
        async with aiohttp.ClientSession() as session:
            for coin_id in coin_id_list:
                url = f"{CoinAPI.COIN_API_BASE_URL}/v1/assets/{coin_id}"
                actions.append(session.get(url, headers=CoinAPI.headers))
                #  Gathers all the asynchronous tasks in actions and waits for 
                #  them to complete concurrently, executing all HTTP request simultaneously.

            coins = await asyncio.gather(*actions)
            for response in coins:
                coins_list.append(CoinAPI._handle_response(response))

        return coins_list
    
    

