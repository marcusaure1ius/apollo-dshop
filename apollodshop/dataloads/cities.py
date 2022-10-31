from typing import List

import pandas as pd

from aiographql.client import GraphQLResponse
from tqdm import tqdm

def get_cities_info(data: GraphQLResponse) -> List:

    cities_raw = data['dshopMain']['cities']

    cities_raw_list = []
    delivery_points_raw_list = []

    for el in tqdm(range(len(cities_raw))):

        cities_raw_list.append({

            'city_id': cities_raw[el]['id'],
            'name': cities_raw[el]['name'],
            'min_free_delivery_price_courier': cities_raw[el]['minFreeDeliveryPriceCourier'],
            'min_free_delivery_price_dp': cities_raw[el]['minFreeDeliveryPriceDp']
        })

        for el2 in range(len(cities_raw[el]['deliveryPoints'])):
            delivery_points_raw_list.append({
                'city_id': cities_raw[el]['id'],
                'id': cities_raw[el]['deliveryPoints'][el2]['id'],
                'address': cities_raw[el]['deliveryPoints'][el2]['address'],
                'delivery_date': cities_raw[el]['deliveryPoints'][el2]['deliveryDate'],
                'has_dressing_room': cities_raw[el]['deliveryPoints'][el2]['hasDressingRoom'],
                'latitude': cities_raw[el]['deliveryPoints'][el2]['latitude'],
                'longitude': cities_raw[el]['deliveryPoints'][el2]['longitude'],
                'time_from': cities_raw[el]['deliveryPoints'][el2]['timeFrom'],
                'time_to': cities_raw[el]['deliveryPoints'][el2]['timeTo']
            })

    cities = pd.DataFrame(cities_raw_list)
    deliv_points = pd.DataFrame(delivery_points_raw_list)

    delivery_points = deliv_points.merge(cities, how='left', left_on='city_id', right_on='city_id')

    return delivery_points.values.tolist()