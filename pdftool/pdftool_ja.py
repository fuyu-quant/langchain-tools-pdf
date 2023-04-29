from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm
import os
from reportlab.lib.colors import deeppink, yellow
from reportlab.platypus import Paragraph, Spacer, PageBreak, FrameBreak, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle, ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT


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
        pdf_llm = OpenAI(temperature=0, model_name=model_name)


        # タイトル作成
        prompt1 = """
        {query}の書類を作る上で適切な日本語のタイトルを教えてください．出力はタイトルのみでお願いします．
        """.format(query=query)
        title = pdf_llm(prompt1)


        # コンテンツ作成
        tools = load_tools(["serpapi"])
        agent = initialize_agent(
            llm = pdf_llm, 
            tools = tools, 
            agent="zero-shot-react-description",
            verbose=True, 
            )

        prompt2 = """
        {query}について必要なことを検索し，内容を500字以内で日本語でまとめてください．
        検索は一回のみでお願いします．
        """.format(query=query)

        text = agent.run(prompt2)

        split_text = [text[x:x+3] for x in range(0, len(text), 50)]

        for i in split_text:
            input_text += i + "<br/>\n"




        # PDFファイルの作成
        p = SimpleDocTemplate("sample.pdf", pagesize=portrait(A4))
        p.setFont('HeiseiMin-W3', size = 5*mm)


        # スタイルの指定
        styles                  = getSampleStyleSheet()
        my_style                = styles['Normal']
        my_style.fontSize       = 6*mm
        my_style.leading        = 10*mm # 段落内の行間

        story                   = [Spacer(1, 10 * mm)]

        p.drawString(30, 800, title)

        story.append( Paragraph(input_text, my_style) )
        story.append( Spacer(1, 3 * mm) )

        p.build(story)


        # 文字列の挿入
        #c.drawString(30, 800, title)
        #c.drawString(30, 600, text)
        
        #c.showPage()
        #c.save()

        result = "PDFファイルを作成したので実行を終了します．"
        return result

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")