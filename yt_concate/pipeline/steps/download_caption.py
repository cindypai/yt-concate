import os
import time

from pytube import YouTube

# from multiprocessing import Process
import concurrent.futures
from .step import Step
import logging
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        start = time.time()

        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            executor.submit(self.downloading, data, inputs, utils)

        # processes = []
        # for i in range(2):
        #     print('processing')
        #     processes.append(Process(target=self.downloading(data, utils)))
        #
        # if __name__ == '__main__':
        #     for process in processes:
        #         process.start()
        #     for process in processes:
        #         process.join()

        end = time.time()
        logger.info(f'took, {end - start} , seconds')

        return data



    def downloading(self, data, inputs, utils):
        for yt in data:
            logger = logging.getLogger()
            logger.info('downloading caption for', yt.id)
            if inputs['fast'] and utils.caption_file_exists(yt):
                logger.info('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                logger.error(f'Error when downloading caption for {yt.url}')
                continue

            #save the caption to a file
            text_file = open(yt.get_caption_filepath(), "w")
            text_file.write(en_caption_convert_to_srt)
            text_file.close()











