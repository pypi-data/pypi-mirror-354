import httpx
from autogenai.core.base import BaseLLM
from autogenai.utils.logger import get_logger
from autogenai.utils.config import get_env, DEFAULT_MODELS
from autogenai.utils.errors import MissingAPIKeyError, LLMResponseError

logger = get_logger("OpenAIEngine")

class OpenAIEngine(BaseLLM):
    def __init__(self, model: str = None):
        try:
            self.api_key = get_env("OPENAI_API_KEY", required=True)
        except EnvironmentError:
            raise MissingAPIKeyError("OPEN_API_KEY is required but not set.")
        self.model = model or DEFAULT_MODELS["openai"]
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.client = httpx.Client(timeout=10)
        logger.info(f"OpenAIEngine initialized with model: {model}")

    def chat(self, prompt: str) -> str:
        return self._send_request(prompt, async_mode=False)
    
    async def achat(self, prompt: str) -> str:
        return await self._send_request(prompt, async_mode=True)
        
    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text:\n\n{text}"
        return self.chat(prompt)

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _prepare_payload(self, prompt: str):
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

    def _send_request(self, prompt: str, async_mode:bool = False):
        headers = self._get_headers()
        data = self._prepare_payload(prompt)

        try:
            logger.info("Sending chat request...")
            if async_mode:
                return self._async_post(data, headers)
            else:
                response = self.client.post(self.api_url, headers=headers, json=data)
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
                logger.info("Received response.")
                return reply.strip()  
            
        except httpx.HTTPError as e:
            logger.error(f"OpenAI chat error: {e}\n")
            raise LLMResponseError(f"OpenAI API Error: {e}", status_code=e.response.status_code, response_data=e.response.json())
        
        except httpx.RequestError as e:
            raise LLMResponseError(f"OpenAI Request Failed: {e}")

    async def _async_post(self, data, headers):
        try:
            response = await self.async_client.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            logger.info("Received response.")
            return reply.strip()
        
        except httpx.HTTPError as e:
            logger.error(f"OpenAI chat error: {e}\n")
            raise LLMResponseError(f"OpenAI API Error: {e}", status_code=e.response.status_code, response_data=e.response.json())
        
        except httpx.RequestError as e:
            raise LLMResponseError(f"OpenAI Request Failed: {e}")

        