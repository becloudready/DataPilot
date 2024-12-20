from .base import TextGenBase
import logging

logger = logging.getLogger(__name__)

class HuggingFaceClient(TextGenBase):
    def override_server_url(self, server_url):
        logger.info("Overriding server URL for HuggingFace")
        return f"http://{server_url}/v1/chat/completions"

    def construct_sql_payload(self, user_question, db_schema):
        prompt = (
            "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n"
            f"Generate a SQL query only to answer this question without explanation: `{user_question}`\n"
            "DDL statements:\n"
            f"{db_schema}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        return {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
    
    def construct_generic_payload(self, user_question):
        prompt = user_question
        return {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_new_tokens": 4096,
            "max_length": 4096,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "stream": False,
            "max_tokens": 1024

        }

    def parse_response(self, response):
        logger.info(f"Parsing response of {self.model_name} with TGI")
        return response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
