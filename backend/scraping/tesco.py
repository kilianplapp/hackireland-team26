from patchright.sync_api import sync_playwright

def main(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f'https://www.tesco.ie/groceries/en-IE/search?query={query}')
        
        # Get all product title elements and price elements
        titles = page.query_selector_all("//*/div[2]/h3/a")
        prices = page.query_selector_all("//*/div/div/div/div/div/form/div/div/div[1]/p[1]")
        
        # Combine titles and prices into a dictionary
        products = {}
        for title, price in zip(titles, prices):
            title_text = title.inner_text().strip()
            price_text = price.inner_text().strip()
            products[title_text] = price_text

        print(products)
        #page.screenshot(path=f'example-{p.chromium.name}.png')
        browser.close()

if __name__ == '__main__':
    main("carrots")
