from zs_utils.api.wildberries.base_api import WildberriesAPI


class WildberriesCommonAPI(WildberriesAPI):
    production_api_url = "https://common-api.wildberries.ru/"


class GetWildberriesSellerInfo(WildberriesCommonAPI):
    """
    https://dev.wildberries.ru/en/openapi/api-information#tag/News-API/paths/~1api~1communications~1v1~1news/get
    """

    http_method = "GET"
    resource_method = "api/v1/seller-info"
