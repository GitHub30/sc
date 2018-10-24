import requests
from lxml.html import fromstring, tostring
import csv


def parse(url):
    r = requests.get(url)
    html = fromstring(r.content)
    html.make_links_absolute(url)
    return html


def main():
    products_url = 'https://www.stella-chemifa.co.jp/products/'
    html = parse(products_url)
    category_urls = html.xpath(f'//article//a[starts-with(@href, "{products_url}cat")]/@href')
    rows = []
    for category_url in category_urls:
        html = parse(category_url)
        product_urls = html.xpath(f'//article//a[starts-with(@href, "{category_url}") and not(contains(@href,"#"))]/@href')
        for product_url in product_urls:
            html = parse(product_url)
            # row = [tostring(td, encoding="utf-8").strip()[4:-5].strip().decode('utf-8') for td in
            #        html.xpath('//article//h2|//article//td')]
            row = [td.text_content().replace('\n', '').replace('\r', '') for td in
                   html.xpath('//article//h2|//article//td')]
            print(row)
            rows.append(row)

    with open('some.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r\n')  # 改行コード（\n）を指定しておく
        # writer.writerow(
        #     ['title', 'name', 'english', 'chemical_formula', 'chemical_substances_no', 'cas_no', 'purpose', 'package',
        #      'description', 'sds'])
        writer.writerows(rows)  # 2次元配列も書き込める


if __name__ == '__main__':
    main()
