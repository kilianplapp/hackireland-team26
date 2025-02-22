import requests

def supervalu(query):
    url = f'https://storefrontgateway.supervalu.ie/api/stores/5550/preview?q={query}&popularTake=30'
    response = requests.get(url)
    data = response.json()
    products = []
    for product in data['products']:
        products.append({
            'title': product['name'],
            'price': product['price'],
            'image': product['image']['default']
        })
    return products

if __name__ == '__main__':
    supervalu("carrot")