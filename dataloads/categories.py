from typing import List

from aiographql.client import GraphQLResponse
from tqdm import tqdm


def get_categories_info(data: GraphQLResponse) -> List:
    categ_raw = data['dshopMain']['categories']
    categ_raw_list = []

    for el in tqdm(range(len(categ_raw))):

        for el2 in range(len(categ_raw[el]['children'])):

            cat_id_lvl2 = categ_raw[el]['children'][el2]['id']
            title_lvl2 = categ_raw[el]['children'][el2]['title']
            parent_id = categ_raw[el]['id']
            children = categ_raw[el]['children'][el2]['children']

            for el3 in range(len(categ_raw[el]['children'][el2]['children'])):
                cat_id_lvl3 = categ_raw[el]['children'][el2]['children'][el3]['id']
                title_lvl3 = categ_raw[el]['children'][el2]['children'][el3]['title']
                parent_id = categ_raw[el]['children'][el2]['id']

                categ_raw_list.append({

                    'cat_id_lvl1': categ_raw[el]['id'],
                    'title_lvl1': categ_raw[el]['title'],
                    'image': categ_raw[el]['image'],

                    'cat_id_lvl2': cat_id_lvl2,
                    'title_lvl2': title_lvl2,
                    'parent_id_lvl2': parent_id,

                    'cat_id_lvl3': cat_id_lvl3,
                    'title_lvl3': title_lvl3,
                    'parent_id_lvl3': parent_id
                })

    return categ_raw_list


def get_low_level_categories(categories_list: List) -> List:
    categ_lvl3 = []

    for category in categories_list:
        categ_lvl3.append(category['cat_id_lvl3'])

    return categ_lvl3
