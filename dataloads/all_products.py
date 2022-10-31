import asyncio
from typing import List, Tuple

from aiographql.client import GraphQLResponse
from aiographql.client import GraphQLClient
from tqdm import tqdm

from gql_requests import get_products


def get_all_products(client: GraphQLClient, categories: List) -> Tuple[List, List]:
    """
    ВВ

    :param client:
    :param categories:
    :return:
    """
    error_categories = []
    all_products_by_category_list = []

    # category['category_id'] - Id категории
    # category['total_products'] - Кол-во продуктов в категории

    for category in tqdm(categories):

        current_page = 0  # Устанавливаем положение текущей страницы = 0

        # Условие на проверку категорий, в которых нет продуктов -  по таким не будет запрос данных
        if category['category_id'] == 0:
            print(f"No products in id category = {category['category_id']}")
        else:
            # Вычисляем кол-во страниц, учитывая что максимальное кол-во продуктов на одной странице - 100
            total_pages = category['total_products'] // 100

            while current_page <= total_pages:

                try:
                    # Запрашиваем данные по конкретной категории и текущей странице
                    response = asyncio.run(get_products(int(category['category_id']), current_page, client))
                    data = response.data['search_v2']['products']

                    current_page += 1

                    for prod in range(len(data)):

                        title = data[prod]['title']
                        id = data[prod]['id']
                        min_sell_price = data[prod]['minSellPrice'] / 100
                        min_full_price = data[prod]['minFullPrice'] / 100
                        feedback_quantity = data[prod]['feedbackQuantity']
                        orders_quantity = data[prod]['ordersQuantity']

                        sku_quantity = len(data[prod]['skuList'])

                        available_amount = 0

                        for sku in range(len(data[prod]['skuList'])):
                            temp_amount = data[prod]['skuList'][sku]['availableAmount']
                            available_amount += temp_amount

                        all_products_by_category_list.append({
                            'product_id': id,
                            'categ_id': category['category_id'],
                            'title': title,
                            'min_sell_price': min_sell_price,
                            'min_full_price': min_full_price,
                            'feedback_quantity': feedback_quantity,
                            'orders_quantity': orders_quantity,
                            'sku_quantity': sku_quantity,
                            'available_amount': available_amount

                        })
                except:
                    error_categories.append(category['category_id'])
                    current_page += 1

    return all_products_by_category_list, error_categories