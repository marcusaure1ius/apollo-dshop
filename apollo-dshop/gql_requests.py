from aiographql.client import GraphQLRequest
from aiographql.client import GraphQLResponse
from aiographql.client import GraphQLClient


async def get_dshop_base_info(client: GraphQLClient) -> GraphQLResponse:
    """
    Получение базовой информации по магазину, выводится:

    - Информация по баннерам

    - Иерархия категорий всего магазина

    - Текущие доступные офферы

    - Города доставки и адреса ПВЗ в этих городах

    :param client: клиент GraphQL с информацией о подключении
    :return: Ответ Apollo сервера
    """
    request = GraphQLRequest(
        query="""
        query DshopMain($productsSize: Int!) {
        dshopMain {
            offers {
            id
            title
            productsPage(size: $productsSize) {
                content {
                id
                title
                shortDescription
                photos {
                    link(trans: ORIGINAL) {
                    high
                    __typename
                    }
                    __typename
                }
                skuList {
                    id
                    sellPrice
                    fullPrice
                    __typename
                }
                __typename
                }
                __typename
            }
            __typename
            }
            banners {
            description
            link
            title
            image {
                high
                __typename
            }
            __typename
            }
            cities {
            id
            name
            minFreeDeliveryPriceCourier
            minFreeDeliveryPriceDp
            deliveryPoints {
                id
                address
                deliveryDate
                hasDressingRoom
                latitude
                longitude
                timeFrom
                timeTo
                __typename
            }
            __typename
            }
            categories {
            id
            title
            image {
                high
                low
                __typename
            }
            children {
                title
                id
                children {
                id
                title
                __typename
                parent {
                    id
                }
                }
                __typename
                parent {
                id
                }
            }
            __typename
            }
            __typename
        }
        }
    """
    )
    variables = {"productsSize": 5}
    headers = {"Authorization": "Basic cHNiX3Nob3A6cHNiX3Nob3Bfc2VjcmV0"}

    response = await client.query(request=request, variables=variables, headers=headers)
    return response


async def get_total_product_by_category_id(cat_id: int, client: GraphQLClient) -> GraphQLResponse:
    """
    Получение списка всех категорий с суммраным кол-вом продуктов

    :param cat_id: ИД категории
    :param client: клиент GraphQL с информацией о подключении
    :return: Ответ Apollo сервера
    """
    request = GraphQLRequest(
        query="""
            query getSearch($input: SearchArgs!) {
            search_v2(input: $input) {
                totalProducts
            }
            }
        """
    )

    variables = {
        "input": {"paging": {
            "size": 99,
            "page": 0
        },
            "query": "",
            "sort": {
                "by": "default",
                "order": "descending"
            },
            "dshopFilterCategories": [],
            "dshopCategoryId": cat_id
        }
    }
    headers = {"Authorization": "Basic cHNiX3Nob3A6cHNiX3Nob3Bfc2VjcmV0"}

    return await client.query(request=request, variables=variables, headers=headers)


async def get_products(categ_id: int, page: int, client: GraphQLClient) -> GraphQLResponse:
    """
    Получение всех продуктов выбранной категории

    :param categ_id: ИД категории
    :param page: Номер страницы
    :param client: клиент GraphQL с информацией о подключении
    :return: Ответ Apollo сервера
    """
    request = GraphQLRequest(
        query="""
            query getSearch($input: SearchArgs!) {
            search_v2(input: $input) {
                products {
                title
                id
                skuList {
                    sellPrice
                    fullPrice
                    id
                    __typename
                    availableAmount
                }
                minSellPrice
                __typename
                feedbackQuantity
                minFullPrice
                ordersQuantity
                }
                totalProducts
                prices {
                max
                min
                __typename
                }
                __typename
            }
            }
        """
    )

    variables = {
        "input": {
            "paging": {
                "size": 100,
                "page": page
            },
            "query": "",
            "dshopCategoryId": categ_id
        }
    }
    headers = {"Authorization": "Basic cHNiX3Nob3A6cHNiX3Nob3Bfc2VjcmV0"}

    return await client.query(request=request, variables=variables, headers=headers)
