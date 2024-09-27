import scrapy
from time import sleep


class LinkedInJobsSpider(scrapy.Spider):
    name = 'linkedin_jobpost'
    retry_delay = 5
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,  # Número de tentativas
        'RETRY_HTTP_CODES': [301, 302, 500, 502, 503, 504, 429],  # Códigos HTTP que acionam retry
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 10

    
    }

    

    def start_requests(self):
        start_urls = [
        "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/3998250173",
        "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/4006008648",
        "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/4017585578",]

    
        for url in start_urls:
            sleep(3)
            yield scrapy.Request(url, callback=self.parse, meta={'dont_redirect': True, 'download_delay': self.retry_delay}, dont_filter=True)


    def parse(self, response):
        
        # Extrair todo o texto do body
        details = response.css('div.decorated-job-posting__details ::text').getall()

        # Verifica se o conteúdo foi extraído
        if not details:
            self.logger.error(f"Nenhum texto extraído de {response.url}")

        # Junta todos os textos extraídos em uma string única
        details_text = ' '.join([text.strip() for text in details if text.strip()])

        # Salva ou imprime o resultado extraído
        yield {
            'url': response.url,
            'details': details_text
        }
