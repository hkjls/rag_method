#use a ai model to embed the summary of the extracted data
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Summarizer:
    def __init__(self):
        self._summarize_chain = None
        self._text_summaries = None
        self._tables_summaries = None

    @property
    def summarize_chain(self):
        return self._summarize_chain

    @summarize_chain.setter
    def summarize_chain(self, prompt):
        try:
            prompt = ChatPromptTemplate.from_template(prompt)
            model = ChatGroq(temperature=0.5, model="model_name")
            self._summarize_chain = prompt| model | StrOutputParser()
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
