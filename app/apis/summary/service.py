from app.core.logger import log_excution_time
from app.core.config import get_settings
from app.apis.summary.schema import SUMMARYResponseSchema

import requests
from summa.summarizer import summarize
from bs4 import BeautifulSoup as bs

class SUMMARYService:
    def __init__(self):
        self.settings = get_settings()
        self.summary = self.settings.summary

        self.prompt = f"""summarize input_text to 4 question in 3
            What is already known on this topic?
            
            What question this study addressed?
            
            What this study adds to out knowledge?
            
            How this is relevant to clinical practice?

            !! Make sure to keep the tag in the example and print it out. But please answer without questions !!

            and find complex terms, with explain
            
            example : 
            
            <knowntopic>
            What is already known on this topic?
            answer ...
            </knowntopic>
            <questionstudy>
            What question this study addressed?
            answer ...
            </questionstudy>
            <studyknowledge>
            What this study adds to out knowledge?
            answer ...
            </studyknowledge>
            <relevantpractice>
            How this is relevant to clinical practice?
            answer ...
            </relevantpractice>
            <complexterms>
            embonpoint : the bodily property of being well rounded
            pabulum : insipid intellectual nourishment
            ...
            </complexterms>
            """
        self.url = "https://api.hyperbolic.xyz/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.summary.model_key}"
        }

    @log_excution_time
    async def run_summary_process(self, text: str):

        split_token_len = 23000

        input_text = ''

        for i in range(4):

            splited_text = text[i * split_token_len : (i + 1) * split_token_len]

            summarized_text = summarize(splited_text, ratio = 0.25)

            if summarized_text == '':

                result = f"text is short to summarize it!"

                response = SUMMARYResponseSchema(text=result)

                return response

            input_text += summarized_text

        data = {
        "messages": [
            {
                "role": "assistant", 
                "content": f"{self.prompt}"},
            {
                "role": "user",
                "content": f"input_text : {input_text}"
            }
        ],
        "model": f"{self.summary.model_name}",
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        response_text = response.json()['choices'][0]['message']['content']

        response_html = bs(response_text, 'html.parser')

        result = ''

        known_topic = response_html.find('knowntopic').get_text()
        question_study = response_html.find('questionstudy').get_text()
        study_knowledge = response_html.find('studyknowledge').get_text()
        relevant_practice = response_html.find('relevantpractice').get_text()
        complex_terms = response_html.find('complexterms').get_text()

        result += f"- {known_topic.strip()}\n\n"
        result += f"- {question_study.strip()}\n\n"
        result += f"- {study_knowledge.strip()}\n\n"
        result += f"- {relevant_practice.strip()}\n\n"
        result += f"[complex term]\n{complex_terms.strip()}"

        response = SUMMARYResponseSchema(text=result)

        return response