from dataclasses import dataclass
import requests


@dataclass
class RatesResponse:
    disclaimer: str
    license: str
    timestamp: int
    base: str
    rates: dict[str, float]


class Client(object):
    def __init__(self, app_id, api_base="https://openexchangerates.org/api/"):
        self.api_base = api_base.rstrip("/")
        self.app_id = app_id
        self.session = requests.Session()

    def get_latest(self, base=None, symbols=None) -> RatesResponse:
        """
        Get latest data.
        ref. https://oxr.readme.io/docs/latest-json
        """
        return RatesResponse(**self.__get_exchange_rates("latest.json", base, symbols))

    def __request(self, endpoint, payload=None):
        url = self.api_base + "/" + endpoint
        request = requests.Request("GET", url, params=payload)
        prepared = request.prepare()

        response = self.session.send(prepared)
        if response.status_code != requests.codes.ok:
            raise OXRStatusError(request, response)
        json = response.json()
        if json is None:
            raise OXRDecodeError(request, response)
        return json

    def __get_exchange_rates(self, endpoint, base, symbols, payload=None):
        if payload is None:
            payload = dict()
        payload["app_id"] = self.app_id
        if base is not None:
            payload["base"] = base
        if isinstance(symbols, list) or isinstance(symbols, tuple):
            symbols = ",".join(symbols)
        if symbols is not None:
            payload["symbols"] = symbols
        return self.__request(endpoint, payload)


class OXRError(Exception):
    """Open Exchange Rates Error"""

    def __init__(self, req, resp):
        super(OXRError, self).__init__()
        self.request = req
        self.response = resp


class OXRStatusError(OXRError):
    """API status code error"""

    pass


class OXRDecodeError(OXRError):
    """JSON decode error"""

    pass
