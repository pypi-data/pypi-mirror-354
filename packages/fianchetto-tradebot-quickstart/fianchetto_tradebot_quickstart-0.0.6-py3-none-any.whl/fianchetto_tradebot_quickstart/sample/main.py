import configparser
import os
from enum import Enum
from time import sleep

import requests
from fianchetto_tradebot.common_models.brokerage.brokerage import Brokerage
from fianchetto_tradebot.server.moex.serving.moex_rest_service import MoexRestService
from fianchetto_tradebot.server.orders.serving.orders_rest_service import OrdersRestService
from fianchetto_tradebot.server.quotes.serving.quotes_rest_service import QuotesRestService

from runnable_service import RunnableService
from concurrent.futures import ThreadPoolExecutor

config = configparser.ConfigParser()
ACCOUNT_ID_KEY = 'ACCOUNT_ID_KEY'
ACCOUNT_KEY = 'ACCOUNT_ID'
ETRADE_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), './config/etrade_config.ini')
SCHWAB_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), './config/schwab_config.ini')
IKBR_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), './config/ikbr_config.ini')

ACCOUNTS_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), './config/accounts.ini')
SERVICE_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), './config/service_config.ini')


services: list[RunnableService] = []
executor = ThreadPoolExecutor(max_workers=10)

class ServiceKey(Enum):
    ORDERS = "orders"
    QUOTES = "quotes"
    MOEX = "moex"
    TRIDENT = "trident"
    HELM = "helm"

def start_all_services():
    # Get all configurations
    credential_dict: dict[Brokerage, str] = {
        Brokerage.ETRADE : ETRADE_CONFIGURATION_FILE,
        Brokerage.SCHWAB : SCHWAB_CONFIGURATION_FILE,
        Brokerage.IKBR : IKBR_CONFIGURATION_FILE
    }

    config.read(SERVICE_CONFIGURATION_FILE)
    ports_dict: dict[ServiceKey, int] = {
        ServiceKey.ORDERS : config.getint('PORTS', 'ORDERS_SERVICE_PORT'),
        ServiceKey.QUOTES : config.getint('PORTS', 'QUOTES_SERVICE_PORT'),
        ServiceKey.TRIDENT :config.getint('PORTS', 'TRIDENT_SERVICE_PORT'),
        ServiceKey.HELM : config.getint('PORTS', 'HELM_SERVICE_PORT'),
        ServiceKey.MOEX : config.getint('PORTS', 'MOEX_SERVICE_PORT')
    }
    invoke_orders_service(credential_dict, ports_dict[ServiceKey.ORDERS])
    invoke_quotes_service(credential_dict, ports_dict[ServiceKey.QUOTES])
    invoke_moex_service(credential_dict, ports_dict[ServiceKey.MOEX])# TODO: Add the rest of the services

    print("Up & Running!")

def invoke_orders_service(credential_dict: dict[Brokerage, str], port=8080):
    orders_service = OrdersRestService(credential_config_files=credential_dict)
    orders_runnable = RunnableService(port, orders_service)

    services.append(orders_runnable)
    executor.submit(orders_runnable)

def invoke_quotes_service(credential_dict: dict[Brokerage, str], port=8081):
    quotes_service = QuotesRestService(credential_config_files=credential_dict)
    quotes_runnable = RunnableService(port, quotes_service)

    services.append(quotes_runnable)
    executor.submit(quotes_runnable)

def invoke_moex_service(credential_dict: dict[Brokerage, str], port=8082):
    moex_service = MoexRestService(credential_config_files=credential_dict)
    moex_runnable = RunnableService(port, moex_service)

    services.append(moex_runnable)
    executor.submit(moex_runnable)

def get_orders():
    config.read(ACCOUNTS_CONFIGURATION_FILE)
    accounts_dict: dict[Brokerage, str] = {
        Brokerage.ETRADE : config.get('ETRADE', ACCOUNT_ID_KEY, fallback=None),
        Brokerage.IKBR : config.get('IKBR', ACCOUNT_KEY, fallback=None),
        Brokerage.SCHWAB : config.get('SCHWAB', ACCOUNT_KEY, fallback=None)
    }

    e_trade_account_id = accounts_dict[Brokerage.ETRADE]

    print(f'Hi, we\'re going list orders for {Brokerage.ETRADE}')  # Press ⌘F8 to toggle the breakpoint.
    host='0.0.0.0'
    port=8080
    uri = f"http://localhost:{port}/api/v1/{Brokerage.ETRADE.value}/accounts/{e_trade_account_id}/orders"
    print(uri)
    response = requests.get(uri)

    print(response)


if __name__ == '__main__':
    start_all_services()
    sleep(5)
    get_orders()
