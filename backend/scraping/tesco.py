from patchright.sync_api import sync_playwright


def tesco(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://www.tesco.ie/groceries/en-IE/search?query={query}")

        # Get all product title elements and price elements
        product_boxes = page.query_selector_all(
            '//*[@id="product-list"]/div[2]/div[4]/div/div/div[2]/div/ul/li'
        )

        products = []
        for product_box in product_boxes:
            title = product_box.query_selector("//*/div[2]/h3/a")
            price = product_box.query_selector(
                "//*/div/div/div/div/div/form/div/div/div[1]/p[1]"
            )
            image = product_box.query_selector("//img")

            title_text = title.inner_text().strip() if title else "No title"
            price_text = price.inner_text().strip() if price else "€0.00"
            image_src = (
                image.get_attribute("srcset").split(" ")[0] if image else "No image"
            )

            products.append(
                {"title": title_text, "price": price_text, "image": image_src}
            )
        # page.screenshot(path=f'example-{p.chromium.name}.png')
        browser.close()
        return products


if __name__ == "__main__":
    print(tesco("carrots"))
