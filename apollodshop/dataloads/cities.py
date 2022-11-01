from typing import List

from aiographql.client import GraphQLResponse
from tqdm import tqdm


def get_cities_info(data: GraphQLResponse) -> List:
    cities_raw = data['dshopMain']['cities']

    delivery_points_raw_list = []

    for el in tqdm(range(len(cities_raw))):

        for el2 in range(len(cities_raw[el]['deliveryPoints'])):
            delivery_points_raw_list.append({
                'city_id': cities_raw[el]['id'],
                'name': cities_raw[el]['name'],
                'min_free_delivery_price_courier': cities_raw[el]['minFreeDeliveryPriceCourier'],
                'min_free_delivery_price_dp': cities_raw[el]['minFreeDeliveryPriceDp'],
                'id': cities_raw[el]['deliveryPoints'][el2]['id'],
                'address': cities_raw[el]['deliveryPoints'][el2]['address'],
                'delivery_date': cities_raw[el]['deliveryPoints'][el2]['deliveryDate'],
                'has_dressing_room': cities_raw[el]['deliveryPoints'][el2]['hasDressingRoom'],
                'latitude': cities_raw[el]['deliveryPoints'][el2]['latitude'],
                'longitude': cities_raw[el]['deliveryPoints'][el2]['longitude'],
                'time_from': cities_raw[el]['deliveryPoints'][el2]['timeFrom'],
                'time_to': cities_raw[el]['deliveryPoints'][el2]['timeTo']
            })

    return delivery_points_raw_list
