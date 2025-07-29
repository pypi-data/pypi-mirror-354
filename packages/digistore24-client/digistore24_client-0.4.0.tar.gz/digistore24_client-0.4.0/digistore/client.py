import dataclasses
import enum
import time
import urllib.parse

import dacite
import requests

import digistore.model as dm


class DigistoreRoutes:
    def __init__(
        self,
        base_url: str='https://digistore24.com/api/call',
    ):
        self.base_url = base_url

    def _url(self, suffix, args: dict=None):
        url = f'{self.base_url}/{suffix}'

        if args:
            args = {
                k: v for k,v in args.items()
                if v is not None # digistore prefers omitted values rather than None/null
            }
            url += f'?{urllib.parse.urlencode(args)}'

        return url

    def create_product(self, product: dm.ShortProduct):
        raw = {
            f'data[{k}]': v for k,v in dataclasses.asdict(product).items()
        }

        return self._url(
            'createProduct',
            raw,
        )

    def get_product(self, product_id, /):
        return self._url('getProduct', {'product_id': product_id})

    def get_purchase(self, args: dict):
        return self._url('getPurchase', args)

    def list_products(self):
        return self._url('listProducts')

    def list_transactions(self, args: dict):
        return self._url(
            'listTransactions',
            args,
        )

    def update_product(self, product: dm.ShortProduct, product_id):
        raw = {
            f'data[{k}]': v for k,v in dataclasses.asdict(product).items()
        }
        raw['product_id'] = product_id

        return self._url(
            'updateProduct',
            raw,
        )



class DigistoreError(Exception):
    pass


def to_response(
    resp: dict | dm.Response | requests.Response, /
) -> dm.Response:
    if isinstance(resp, dm.Response):
        return resp

    if isinstance(resp, requests.Response):
        resp = resp.json()

    return dacite.from_dict(
        data_class=dm.Response,
        data=resp,
        config=dacite.Config(
            cast=(int, float, enum.Enum),
        ),
    )


def check_response(resp: dict | dm.Response, /):
    if not to_response(resp).successful:
        raise DigistoreError(resp)

    return resp


def checked_response(resp: dict | dm.Response | requests.Response) -> dm.Response:
    if not resp.ok:
        print('Error:')
        print(resp.text)
    resp.raise_for_status()
    resp = to_response(resp)
    check_response(resp)

    return resp


class DigistoreClient:
    def __init__(
        self,
        api_key: str,
        routes: DigistoreRoutes=DigistoreRoutes()
    ):
        self.api_key = api_key
        self.routes = routes

        self.sess = requests.Session()
        sess = self.sess
        sess.headers = {
            'Accept': 'application/json',
            'X-DS-API-KEY': self.api_key,
        }

    def create_product(self, product: dm.ShortProduct, /) -> int:
        '''
        creates new product. If successful, created product-id is returned, otherwise, raises
        DigistoreError
        '''
        url = self.routes.create_product(product)

        res = checked_response(self.sess.get(url))

        product_id = res.data['product_id']

        return product_id

    def get_product(self, product_id: int, /) -> dm.Product:
        url = self.routes.get_product(product_id)

        res = self.sess.get(url)
        res = checked_response(res)

        def to_int(v):
            if isinstance(v, int):
                return v

            if not v:
                return None

            return int(v)

        def to_float(v):
            if isinstance(v, float):
                return v

            if not v:
                return None

            return float(v)

        return dacite.from_dict(
            data_class=dm.Product,
            data=res.data,
            config=dacite.Config(
                cast=(enum.Enum, dm.DigiBool),
                type_hooks={
                    int: to_int,
                    float: to_float,
                },
            ),
        )

    def update_product(self, product: dm.ShortProduct, product_id):
        res = self.sess.get(
            self.routes.update_product(
                product=product,
                product_id=product_id,
            ),
        )
        res = checked_response(res)
        return res

    def list_products(self):
        res = self.sess.get(self.routes.list_products())

        res = to_response(res)

        data = res.data
        products = data['products']

        return [
            dacite.from_dict(
                data_class=dm.Product,
                data=product_dict,
                config=dacite.Config(
                    cast=[int, float, dm.DigiBool],
                ),
            ) for product_dict in products
        ]

    def list_transactions(
        self,
        args: dict,
        remaining_retries: int=3,
    ) -> list[dict]:
        url = self.routes.list_transactions(args=args)

        res = to_response(self.sess.get(url))

        if res.result is dm.ResultStatus.ERROR:
            if remaining_retries == 0:
                raise DigistoreError(res)

            time.sleep(3)

            return self.list_transactions(
                args=args,
                remaining_retries=remaining_retries - 1,
            )

        return res.data.get('transaction_list')


def default_client():
    import digistore.cfg
    return DigistoreClient(api_key=digistore.cfg.config().api_key)
