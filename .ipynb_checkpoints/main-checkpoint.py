import pandas as pd
import numpy as np
import asyncio
import logging

from dadata import Dadata
from folium.plugins import MarkerCluster
from tqdm.notebook import tqdm
from aiographql.client import GraphQLClient

from gql_requests import get_dshop_base_info

from settings import ENDPOINT_URL, DADATA_TOKEN, DADATA_SECRET

from dataloads.banners import get_banners_info
from dataloads.categories import get_categories_info, get_low_level_categories
from dataloads.cities import get_cities_info
from dataloads.total_products import get_total_products_info
from dataloads.all_products import get_all_products

# Create GQL client for requests to Apollo
# Create dadata client to fetch address from Dadata API
# Create logging config
client = GraphQLClient(endpoint=ENDPOINT_URL)
dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Getting base info of PSB Dshop
logging.info('Start requesting data from Apollo')
response = asyncio.run(get_dshop_base_info(client))
data = response.data

# Load banners info
logging.info('Start downloading banners data')
banners = get_banners_info(data)

# Load categories info
logging.info('Start downloading categories data')
categories = get_categories_info(data)

# Load cities & delivery point info
logging.info('Start downloading cities data')
delivery_points = get_cities_info(data)

# Load total product by category id
logging.info('Start downloading total products in each category')
low_level_cats = get_low_level_categories(categories)
total_products = get_total_products_info(client, low_level_cats[0:10])

# Load all product by category id
logging.info('Start downloanding all products in each category')
all_products, errors = get_all_products(client, total_products)