import os
import shutil
from .step import Step
from yt_concate.settings import CAPTIONS_DIR
from yt_concate.settings import VIDEOS_DIR
import logging

class DeleteDownloadedFile(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        if inputs['cleanup']:
            try:
                shutil.rmtree(CAPTIONS_DIR)
                shutil.rmtree(VIDEOS_DIR)
            except OSError as e:
                logger.warning(f'Error: {e}')

            logger.info('downloaded files have been deleted')