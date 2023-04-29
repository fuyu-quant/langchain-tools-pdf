from langchain.tools import BaseTool


class PDFTool(BaseTool):
    name = "lgbm_train_tool"
    description = """useful to receive csv file name and learn LightGBM"""

    def _run(self, query: str) -> str:
      """Use the tool."""
      
      return result

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")