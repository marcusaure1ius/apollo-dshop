import asyncio
from typing import List

from aiographql.client import GraphQLClient
from tqdm import tqdm

from gql_requests import get_total_product_by_category_id


def get_total_products_info(client: GraphQLClient, categories: List) -> List:
    categories_with_total_products_list = []

    for category in tqdm(categories):
        category_id = category
        response = asyncio.run(get_total_product_by_category_id(int(category), client))
        total_products = response.data

        categories_with_total_products_list.append({
            'category_id': category_id,
            'total_products': total_products['search_v2']['totalProducts']
        })

    return categories_with_total_products_list
