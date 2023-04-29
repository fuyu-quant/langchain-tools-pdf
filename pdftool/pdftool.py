from reportlab.pdfgen import canvas


from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm


from langchain.tools import BaseTool


# 文字コードの指定
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))


class PDFTool(BaseTool):
    name = "PDFTool"
    description = """It is useful for creating PDF files. The input is the content of the PDF file to be created."""

    def _run(self, query: str) -> str:
      """Use the tool."""

      c = canvas.Canvas("report.pdf")

      c.setFont('HeiseiMin-W3', size = 5*mm)


      # 文字列の挿入
      c.drawString(30, 800, "LightGBMの学習結果")
      c.drawString(30, 600, "accuracy")
      
      

      result = "PDF file has been created."
      return result

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")