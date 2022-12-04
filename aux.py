import requests
from bs4 import BeautifulSoup as bs

class GetWebData:

    @staticmethod
    def request_data(url: str) -> requests.Response:

        return requests.get(url=f'{url}')
        

    @staticmethod
    def parse_data(requested_data: requests.Response) -> bs:

        return bs(markup=requested_data.text, features='html.parser')