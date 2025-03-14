#use a ai model to embed the summary of the extracted data
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Summarizer:
    def __init__(self, model_name, prompt, api_key):#instruction?
        self._text_summaries = None
        self._tables_summaries = None

        try:
            prompt = ChatPromptTemplate.from_template(prompt)
            # model = ChatGroq(
            #     temperature=0.5, 
            #     model_name=model_name,
            #     # groq_api_base="https://integrate.api.nvidia.com/v1",
            #     groq_api_key=api_key
            # )

            model = ChatNVIDIA(
                model=model_name,
                api_key=api_key, 
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
            )

            self._summarize_chain = prompt | model | StrOutputParser()
        except TypeError as e:
            print(e)

    @property
    def text_summaries(self):
        return self._text_summaries
    
    @text_summaries.setter
    def text_summaries(self, texts):
        self._text_summaries = self._summarize_chain.batch(texts, {"max_concurrency":3})

    # Summarize tables
    @property
    def tables_summaries(self):
        return self._tables_summaries

    @tables_summaries.setter
    def tables_summaries(self, tables):
        tables_html = [table.metadata.text_as_html for table in tables]
        self._tables_summaries = self._summarize_chain.batch(tables_html, {"max_concurrency":3})
    

if __name__ == "__main__":

    from pathlib import Path
    from dotenv import load_dotenv
    import os
    from extractor import extractor

    root = Path(__file__).resolve().parent.parent.parent
    file = f"{root}/media/Demographie-Antananarivo.pdf"
    load_dotenv()
    # Prompt
    prompt_text = """
    You are an assistant tasked with summarizing tables and text.
    Give a concise summary of the table or text.

    Respond only with the summary, no additionnal comment.
    Do not start your message by saying "Here is a summary" or anything like that.
    Just give the summary as it is.

    Table or text chunk: {element}

    """
    sum = Summarizer("meta/llama-3.3-70b-instruct", prompt_text, os.getenv("SECRET_KEY"))
    data_file = extractor()
    data_file.chunks = file

    data_file.tt = data_file.chunks

    sum.text_summaries = data_file.tt["texts"]
    sum.text_summaries = data_file.tt["tables"]
