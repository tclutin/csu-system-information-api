import httpx

from config.config import settings
from dto.faq_dto import SearchFAQDTO


class FAQFinderService:
    async def search_faqs(self, dto: SearchFAQDTO):
        data = {
            "message": dto.message,
            "top_k": dto.top_k,
            "min_similarity": dto.min_similarity,
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(settings.faqfinder_service_url + "/query", json=data)
                response.raise_for_status()
                body = response.json()
                return body
            except Exception:
                raise ValueError("FAQFINDER_SERVICE: я чуток откис, ты там это.. держись")

    async def update_faqs(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(settings.faqfinder_service_url + "/update")
                response.raise_for_status()
                body = response.json()
                return body
            except Exception:
                raise ValueError("FAQFINDER_SERVICE: я чуток откис, ты там это.. держись")

