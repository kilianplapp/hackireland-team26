import requests

def dunnes(query):
    url = f'https://storefrontgateway.dunnesstoresgrocery.com/api/stores/258/preview?q={query}&popularTake=30'
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
    dunnes("carrot")