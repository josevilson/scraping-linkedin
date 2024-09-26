import json

import scrapy
from scrapy_splash import SplashRequest


class LinkedInJobsSpider(scrapy.Spider):
    name = 'linkedin_jobs_spider'

    def start_requests(self):
        base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/'
        for start in range(0, 1001, 10):  # Exemplo para 10 páginas
            url = f'{base_url}?keywords=Engenheiro+De+Dados&location=S%C3%A3o+Paulo%2C+S%C3%A3o+Paulo%2C+Brasil&geoId=104746682&refresh=true&position=1&pageNum=0&start={start}'
            yield SplashRequest(url, self.parse, args={'wait': 5})

    def parse(self, response):
        job_cards = response.css('div.base-card')
        jobs = []

        for card in job_cards:
            title = card.css(
                'h3.base-search-card__title::text').get(default="Título não encontrado").strip()
            company = card.css(
                'h4.base-search-card__subtitle::text').get(default="Empresa não encontrada").strip()
            location = card.css(
                'span.job-search-card__location::text').get(default="Local não encontrado").strip()
            time_posted = card.css(
                'time.job-search-card__listdate::text').get(default="Tempo não encontrado").strip()
            job_link = card.css(
                'a.base-card__full-link::attr(href)').get(default="Link não encontrado").strip()

            job = {
                "titulo": title,
                "empresa": company,
                "local": location,
                "tempo": time_posted,
                "link_vaga": job_link
            }

            jobs.append(job)

        # Salva os dados em um arquivo JSON
        with open('jobs_new.json', 'a') as f:  # Usando 'a' para adicionar os dados
            json.dump(jobs, f, ensure_ascii=False, indent=4)
            f.write('\n')  # Adiciona uma nova linha após cada grupo de jobs
