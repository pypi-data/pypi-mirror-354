from zs_utils.api.wildberries.base_api import WildberriesAPIN


class WildberriesAdvertiseAPI(WildberriesAPI):
    production_api_url = "https://advert-api.wildberries.ru/"


class GetWildberriesCompanies(WildberriesAdvertiseAPI):
    """
    https://dev.wildberries.ru/openapi/promotion#tag/Kampanii/paths/~1adv~1v1~1promotion~1count/get
    """

    http_method = "GET"
    resource_method = "adv/v1/promotion/count"


class GetWildberriesCompanyReport(WildberriesAdvertiseAPI):
    """
    https://dev.wildberries.ru/openapi/analytics#tag/Statistika-po-prodvizheniyu/paths/~1adv~1v2~1fullstats/post
    """

    http_method = "POST"
    resource_method = "adv/v2/fullstats"
    required_params = ["array_payload"]
    array_payload = True


class GetWildberriesCompanyInfo(WildberriesAdvertiseAPI):
    """
    https://dev.wildberries.ru/openapi/promotion#tag/Kampanii/paths/~1adv~1v1~1promotion~1adverts/post
    """

    http_method = "POST"
    resource_method = "adv/v1/promotion/adverts"
    required_params = ["array_payload"]
    array_payload = True
