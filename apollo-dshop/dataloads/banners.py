from typing import List

from aiographql.client import GraphQLResponse
from tqdm import tqdm

def get_banners_info(data: GraphQLResponse) -> List:
    banners_raw = data['dshopMain']['banners']
    banners_raw_list = []

    for el in tqdm(range(len(banners_raw)), desc='Processing banners data'):
        banners_raw_list.append({

            'desc': banners_raw[el]['description'],
            'link': banners_raw[el]['link'],
            'image_link_high': banners_raw[el]['image']['high'],
            'type_name': banners_raw[el]['__typename']
        })

    return banners_raw_list