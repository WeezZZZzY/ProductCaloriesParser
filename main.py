from bs4 import BeautifulSoup as BS
import json
import csv
import requests

url = "https://calorizator.ru/product"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
req = requests.get(url, headers=headers)
src = req.text

#запись html страницы сайта в файл, что бы не бомбить сайт
with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BS(src, "lxml")

#получение названия категории и ссылки на неё
all_categories_dict = {}
product_category = soup.find("div", {"class": "node-content"}).find_all("li")

for product in product_category:
    name_products = product.find("a")
    link_products = "https://calorizator.ru/" + name_products.get("href")
    
    all_categories_dict[name_products.text] = link_products


#запись категорий продуктов с ссылками в json файл
with open("all_categories_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding="utf-8") as file:
    all_catigories = json.load(file)


for name_products, link_products in all_catigories.items():
    rep = [',', ' ', '-']
    
    for item in rep:
        if item in name_products:
            name_products = name_products.replace(item, "_")
    
    #пробег по ссылкам в категории продуктов, для получения всех продуктов
    req = requests.get(url=link_products, headers=headers)
    src = req.text

    #запись в файл
    with open(f"data/{name_products}.html", "w", encoding="utf-8") as file:
        file.write(src)

    #открытие файла для дальнейше работы
    with open(f"data/{name_products}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BS(src, "lxml")

#находим заголовки таблицы
    table_head = soup.find("div", {"class": "view-content"}).find("table").find("tr").find_all("th")
    title = table_head[1].text
    protein = table_head[2].text
    fat = table_head[3].text
    carbohydrates = table_head[4].text
    kcal = table_head[5].text
    
    #записываем в файл
    with open(f"data/{name_products}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (   
                title,
                protein,
                fat,
                carbohydrates,
                kcal
            )
        )

#собираем данные о продуктах
    products_data = soup.find("div", {"class": "view-content"}).find("table").find("tbody").find_all("tr")

    for item in products_data:
        product_tds = item.find_all('td')
        
        title = product_tds[1].find("a").text.strip()
        protein = product_tds[2].text.strip()
        fat = product_tds[3].text.strip()
        carbohydrates = product_tds[4].text.strip()
        kcal = product_tds[5].text.strip()

    #добавляем в файл
        with open(f"data/{name_products}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (   
                    title,
                    protein,
                    fat,
                    carbohydrates,
                    kcal
                )
            )