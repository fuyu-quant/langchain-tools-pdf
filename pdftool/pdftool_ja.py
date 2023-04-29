from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm


from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from langchain.tools import BaseTool


# 文字コードの指定
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))


class PDFTool_ja(BaseTool):
    name = "PDFTool"
    description = """It is useful for creating PDF files. The input is the content of the PDF file to be created."""

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        model_name="gpt-3.5-turbo"
        llm = OpenAI(temperature=0, model_name=model_name)


        # タイトル作成
        prompt1 = """
        {query}の書類を作る上で適切なタイトルを教えてください．出力はタイトルのみでお願いします．
        """.format(query=query)
        title = llm(prompt1)


        # コンテンツ作成
        tools = load_tools(["serpapi"])
        agent = initialize_agent(
            llm = llm, 
            tools = tools, 
            agent="zero-shot-react-description",
            verbose=True, 
            return_intermediate_steps=True
            )

        prompt2 = """
        {query}について必要なことを検索し，内容を300字以内でまとめてください．
        """.format(query=query)

        text = agent.run(prompt2)




        c = canvas.Canvas("report.pdf")
        c.setFont('HeiseiMin-W3', size = 5*mm)


        # 文字列の挿入
        c.drawString(30, 800, title)
        c.drawString(30, 600, text)
        
        c.showPage()
        c.save()

        result = "PDF file has been created."
        return result

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")