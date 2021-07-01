from .step import Step
from yt_concate.model.found import Found
import logging

class Search(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        search_word = inputs['search_word']

        found = []
        for yt in data:
            captions = yt.captions
            if not captions:
                continue

            for caption in captions:
                if search_word in caption:
                    time = captions[caption]
                    f = Found(yt, caption, time)
                    found.append(f)

        logger.info(f'video found:, {len(found)}')
        return found
