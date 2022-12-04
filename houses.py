# Imports
import requests
import pandas as pd
from aux import GetWebData
from bs4 import BeautifulSoup as bs

page: int = 1
url: str = f'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={page}'

# Making the GET requests and saving it as text
ret: requests.Response = GetWebData.request_data(url=url)
soup: bs = GetWebData.parse_data(requested_data=ret)

# Defining the houses 
houses: soup.ResultSet = soup.find_all(name='a', attrs={'class': 'property-card__content-link js-card-title'})

# Extracting the quantity of houses
qtty_houses: float = float(soup.find(name='strong', attrs={'class': 'results-summary__count'}).text.replace('.', ''))

df = pd.DataFrame(
    columns=['description',
            'address',
            'area',
            'bedrooms',
            'wc',
            'parking_spaces',
            'value',
            'condominium_fee',
            'wlink']
)


# Once we got the data from the first page, we have got to go to the next pages.
while qtty_houses > df.shape[0]:

    # Defining URL and its pages
    page += 1
    url: str = f'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={page}'
    print(f'Pages: {page} \t Quantintiy of houses: {df.shape[0]}')
    
    # Making the GET requests and saving it as text
    ret: requests.Response = GetWebData.request_data(url=url)
    soup: bs = GetWebData.parse_data(requested_data=ret)

    # Houses of the new page
    houses: soup.ResultSet = soup.find_all(name='a', attrs={'class': 'property-card__content-link js-card-title'})

    # For each house in the pages, try to get the specific attribute (addres, description, etc). It that isn't possible, return None
    for house in houses:
        try:
            description: str = house.find(name='span', attrs={'class': 'property-card__title'}).text.strip()
        except:
            description = None
        try:
            address: str = house.find(name='span', attrs={'class': 'property-card__address'}).text.strip()
        except:
            address = None
        try:
            area: str = house.find(name='span', attrs={'class': 'property-card__detail-area'}).text.strip()
        except:
            area = None
        try:
            bedrooms: str = house.find(name='li', attrs={'class': 'property-card__detail-room'}).span.text.strip()
        except:
            bedrooms = None
        try:
            wc: str = house.find(name='li', attrs={'class': 'property-card__detail-bathroom'}).span.text.strip()
        except:
            wc = None
        try:
            parking_spaces: str = house.find(name='li', attrs={'class': 'property-card__detail-garage'}).span.text.strip()
        except:
            parking_spaces = None
        try:
            value: str = house.find(name='div', attrs={'class': 'property-card__price'}).p.text.strip()
        except:
            value = None
        try:
            condominium_fee: str = house.find(name='strong', attrs={'class': 'js-condo-price'}).text.strip()
        except:
            condominium_fee = None
        try:
            wlink: str = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None
        
        df.loc[df.shape[0]] = [
                description,
                address,
                area,
                bedrooms,
                wc,
                parking_spaces,
                value,
                condominium_fee,
                wlink]   

df.to_csv(path_or_buf='houses.csv', sep=',', index=False)