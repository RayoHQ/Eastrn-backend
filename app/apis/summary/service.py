from app.core.logger import log_excution_time
from app.core.config import get_settings
# from app.apis.summary.schemas import SUMMARYResponseSchema

class SUMMARYService:
    def __init__(self):
        self.settings = get_settings()
        self.summary = self.settings.summary


    @log_excution_time
    async def run_summary_process(self, text: str):

        