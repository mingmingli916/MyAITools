import requests
from lxml import etree


def get_msg(url='http://www.tianqi.com/tongzhou/life.html'):
    """
    Crawl daily weather information from the specified url.
    :param url:
    :return: weather information string
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get(url, headers=headers)

    html = response.text

    html_xpath = etree.HTML(html)

    rain = html_xpath.xpath('/html/body/div[4]/div/ul/li/p/text()')[0]
    ultraviolet_ray = html_xpath.xpath('/html/body/div[4]/div/ul/li[3]/p/text()')[0].strip('。')
    clothes = html_xpath.xpath('/html/body/div[4]/div/ul/li[6]/p/text()')[0].strip('。')
    air = html_xpath.xpath('/html/body/div[4]/div/div[3]/dl/dd/b/text()')[0]
    temperature = html_xpath.xpath('/html/body/div[4]/div/div[3]/dl/dd/text()')[0]
    air_quality = html_xpath.xpath('/html/body/div[4]/div/div[3]/dl/dd[2]/b/text()')[0]

    msg = '；\n'.join([rain, ultraviolet_ray, clothes, air, temperature, air_quality, ''])
    return msg
