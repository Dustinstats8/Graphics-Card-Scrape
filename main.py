from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import re


# set user agent info to help with bot detectors on websites (like BestBuy)
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
headers = {'User-Agent': user_agent}


def get_newegg_top3():
    url = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709&Order=3"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # find all product descriptions and prices /// resultset object is returned
    prod_descriptions = soup.findAll('div', class_='item-info')
    # prod_prices = soup.findAll('li', class_='price-current')
    prod_prices = soup.findAll('ul', class_='price')

    # iterate over resultsets and add product title/price to list
    prod_descriptions_list = []
    prod_prices_list = []
    for i in prod_descriptions:
        prod_descriptions_list.append(i.find('a', title='View Details').text)
    for i in prod_prices:
        unwanted = i.find('a', class_='price-current-num')
        try:
            unwanted.extract()
        except AttributeError:
            ""

        prod_prices_list.append(i.find('li', class_='price-current').text)

    newegg_products = {}
    for i in range(3):
        newegg_products[prod_descriptions_list[i]] = prod_prices_list[i]

    return newegg_products


def get_microCenter_top3():
    url = "https://www.microcenter.com/category/4294966937/graphics-cards"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # find all product descriptions and prices /// resultset object is returned
    prod_descriptions = soup.findAll('div', class_='normal')
    prod_prices = soup.findAll('div', class_='price')

    # iterate over resultsets and add product title/price to list
    prod_descriptions_list = []
    prod_prices_list = []
    for i in prod_descriptions:
        prod_descriptions_list.append(i.find('a').text)
    for i in prod_prices:
        prod_prices_list.append(i.find('span').text)

    micro_center_products = {}
    for i in range(3):
        micro_center_products[prod_descriptions_list[i]] = prod_prices_list[i]

    return micro_center_products


def get_bestBuy_top3():
    url = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # find all product descriptions and prices /// resultset object is returned
    prod_descriptions = soup.findAll('div', class_='information')
    prod_prices = soup.findAll('div', class_='priceView-hero-price priceView-customer-price')

    # iterate over resultsets and add product title/price to list
    prod_descriptions_list = []
    prod_prices_list = []
    for i in prod_descriptions:
        prod_descriptions_list.append(i.find('a').text)
    for i in prod_prices:
        prod_prices_list.append(i.find('span').text)

    best_buy_products = {}
    for i in range(3):
        best_buy_products[prod_descriptions_list[i]] = prod_prices_list[i]

    return best_buy_products


def show_top_3():
    # convert to dataframe for easier viewing
    all_products = {'Newegg': get_newegg_top3(), 'Micro Center': get_microCenter_top3(), 'Best Buy': get_bestBuy_top3()}

    print('Most popular graphics cards from online retailers')
    print('---------------------------------------------------')
    for i in all_products:
        print(i, ':')
        for j in all_products[i]:
            print(j, ' - ', all_products[i][j])
        print('---------------------------------------------------\n')


def newegg_4090():
    url = \
        "https://www.newegg.com/msi-geforce-rtx-4090-rtx-4090-gaming-x-trio-24g/p/N82E16814137761?Item=N82E16814137761"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    newegg_price = soup.find('li', class_='price-current').text

    # remove comma, dollar sign, and convert to float for comparison
    newegg_price = re.sub(",", "", newegg_price)
    return float(newegg_price[1:])


def micro_center_4090():
    url = "https://www.microcenter.com/product/659527/msi-nvidia-geforce-rtx-4090-gaming-trio-triple-fan-24-gb-gddr6x-pcie-40-graphics-card"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    micro_center_price = soup.find('span', id='pricing').text

    # remove comma, dollar sign, and convert to float for comparison
    micro_center_price = re.sub(",", "", micro_center_price)
    return float(micro_center_price[1:])


def best_buy_4090():
    url = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-4090-gaming-trio-24g-24gb-ddr6x-pci-express-4-0-graphics-card/6522371.p?skuId=6522371"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    best_buy_price_raw = soup.findAll('div', class_='priceView-hero-price priceView-customer-price')
    for i in best_buy_price_raw:
        best_buy_price = i.find('span').text

    # remove comma, dollar sign, and convert to float for comparison
    best_buy_price = re.sub(",", "", best_buy_price)
    return float(best_buy_price[1:])


def price_comp_4090():
    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.15, 0.5, 0.75])
    y = [int(newegg_4090()), int(micro_center_4090()), int(best_buy_4090())]
    x = ['Newegg', 'Micro Center', 'Best Buy']
    ax.bar(x, y)
    ax.set(ylabel="Price")
    ax.set(title="Cost of RTX 4090 Graphics Cards")
    ax.set_ylim([0, 2000])
    plt.show()


def main():
    show_top_3()
    price_comp_4090()


if __name__ == '__main__':
    main()
