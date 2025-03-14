# from langchain_nvidia_ai_endpoints import ChatNVIDIA
from transformers import AutoProcessor, AutoModelForImageTextToText
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class imageSummarizer:
    def __init__(self, prompt_template, model_name, api_key=""):
        self._images_summaries = None

        try:
            # model = ChatNVIDIA(
            #     model=model_name,
            #     api_key=api_key,
            #     temperature=0.2,
            #     top_p=0.7,
            #     max_tokens=1024,
            # )

            # processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            # processor = AutoProcessor.from_pretrained(model_name)
            # model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-large")
            model = AutoModelForImageTextToText.from_pretrained(model_name)
            
            messages = [
                (
                    "user",
                    [
                        {
                            "type": "text",
                            "text": prompt_template
                        },
                        {
                            "type":"image_url",
                            "image_url":{"url":"data:image/jpeg;base64,{image}"}
                        }
                    ]
                )
            ]

            prompt = ChatPromptTemplate.from_template(messages)
            self._images_chain = prompt | model | StrOutputParser()

        
        except TypeError as e:
            print(e)

    @property
    def images_summaries(self):
        return self.__images_summaries
    
    @images_summaries.setter
    def images_summaries(self):
        return
    

if __name__ == "__main__":
    from pathlib import Path
    from dotenv import load_dotenv
    import os
    from extractor import extractor

    prompt_template = """Describe the image in detail. For context,
                  the image is part of a research paper explaining the transformers
                  architecture. Be specific about graphs, such as bar plots."""
    
    img_sum = imageSummarizer(prompt_template, "Salesforce/blip-image-captioning-large")
    
