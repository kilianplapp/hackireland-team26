from patchright.sync_api import sync_playwright


def aldi(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://groceries.aldi.ie/en-GB/Search?keywords={query}")
        # w wait for the page to load
        page.wait_for_load_state("networkidle")
        # Get all product title elements and price elements
        product_boxes = page.query_selector_all('//*[@id="vueSearchResults"]/div/div')

        products = []
        for product_box in product_boxes:
            title = product_box.query_selector("//div/div[3]/a")
            price = product_box.query_selector("//div/div[4]/div[2]/div/span/span")
            image = product_box.query_selector("//div/div/a/figure/img")

            title_text = title.inner_text().strip() if title else "No title"
            price_text = price.inner_text().strip() if price else "€0.00"
            image_src = image.get_attribute("src") if image else "No image"

            products.append(
                {"title": title_text, "price": price_text, "image": image_src}
            )
        # page.screenshot(path=f'example-{p.chromium.name}.png')
        browser.close()
        return products


if __name__ == "__main__":
    print(aldi("carrots"))
