import datetime
import scrapy
from scrapy_playwright.page import PageCoroutine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip

from tasascrapy.items import RateItem


class TasaBanreserva(scrapy.Spider):
    name = 'tasa-banreserva'

    custom_settings = {
        'FEED_URI': 'rate.csv',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        yield scrapy.Request('https://www.banreservas.com/',
                             meta={'playwright': True})

    def parse(self, response):
        rate = response.css('td.tasacambio-ventaUS::text').get()

        rate = RateItem()
        rate['acronym'] = 'BRD'
        rate['rate_exchange'] = rate
        rate['day'] = datetime.date.today()
        
        # if you want to save in a database. 
        # yield rate
        
        yield {
            'rate_exchange': rate,
            'day': datetime.date.today()
        }


class TasaPopular(scrapy.Spider):
    name = 'tasa-popular'

    custom_settings = {
        'FEED_URI': 'rate.csv',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def __init__(self) -> None:
        self.driver = webdriver.Firefox()

    def start_requests(self):
        yield scrapy.Request('https://popularenlinea.com/personas/Paginas/Home.aspx',
                             meta={'playwright': True})

    def parse(self, response):
        self.driver.get(
            'https://popularenlinea.com/personas/Paginas/Home.aspx')
        self.driver.implicitly_wait(30)

        try:
            # close_window = self.driver.find_element(
            #     By.XPATH, '//span[@class="close_modal_banner BPD-icon2-nav-15 pull-right white_text"]'
            # )

            # close_window.click()

            tasa_btn = self.driver.find_element(
                By.XPATH, '//span[@class="BPD-icon2-pro-35"]')

            tasa_btn.click()

            input_with_dollars = self.driver.find_element(
                By.XPATH, '//input[@id="venta_peso_dolar_desktop"]')
            input_with_dollars.click()
            input_with_dollars.send_keys(Keys.CONTROL, "a")
            input_with_dollars.send_keys(Keys.CONTROL, "c")

            tasa = pyperclip.paste()

            print(f'Tasa: {tasa}')
        except Exception as err:
            print(err)
            print('We have an error. Send an email')
            raise
        else:
            rate = RateItem()
            rate['acronym'] = 'BPD'
            rate['rate_exchange'] = tasa
            rate['day'] = datetime.date.today()
            
            # yield rate
            
            yield {
                'rate_exchange': tasa,
                'day': datetime.date.today()
            }

        self.driver.close()


class TasaBancoBhd(scrapy.Spider):
    name = 'tasa-bancobhd'

    allowed_domains = ['www.bhdleon.com.do']

    custom_settings = {
        'FEED_URI': 'rate.csv',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def __init__(self) -> None:
        self.driver = webdriver.Firefox()

    def start_requests(self):
        yield scrapy.Request('https://bhd.com.do/wps/portal/BHD/Inicio/',
                             meta={'playwright': True})

    def parse(self, response):
        self.driver.get(
            'https://bhd.com.do/wps/portal/BHD/Inicio/')
        self.driver.implicitly_wait(20)

        try:
            exchange_btn = self.driver.find_element(By.XPATH,
                                                    '//a[@class="dialog_opener" and text()="Tasas de Cambio"]'
                                                    )
            exchange_btn.click()

            tasa = response.xpath(
                '//div[@id="TasasDeCambio"]/table/tbody/tr[2]/td[3]/text()'
            ).get()

            str(tasa)
            tasa_formatted = tasa.replace(' DOP', '')
            float(tasa_formatted)

        except Exception as err:
            print(err)
            print('We have an error. Send an email')
            raise
        else:
            rate = RateItem()
            rate['acronym'] = 'BHD'
            rate['rate_exchange'] = tasa_formatted
            rate['day'] = datetime.date.today()
            
            # yield rate
            
            yield {
                'rate_exchange': tasa_formatted,
                'day': datetime.date.today()
            }

        self.driver.close()


class TasaBancoCentral(scrapy.Spider):
    name = 'tasa-bancocentral'

    custom_settings = {
        'FEED_URI': 'rate.csv',
        'FEED_FORMAT': 'csv',
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        yield scrapy.Request('https://www.bancentral.gov.do/',
                             meta={'playwright': True})

    def parse(self, response):
        rate = response.xpath(
            '//html/body/div[4]/row/div[2]/div/div/div/div[3]/div[4]/div/table[1]/tbody/tr/td[2]/h5/text()'
        ).get()

        str(rate)
        rate_formatted = rate.replace(' ', '').replace('\n', '')
        float(rate_formatted)

        rate = RateItem()
        rate['acronym'] = 'BCD'
        rate['rate_exchange'] = rate_formatted
        rate['day'] = datetime.date.today()
        
        # yield rate
        print(rate_formatted)
        
        yield {
            'rate_exchange': rate_formatted,
            'day': datetime.date.today()
        }
