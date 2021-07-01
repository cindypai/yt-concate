
from pytube import YouTube
from .step import Step
from yt_concate.settings import VIDEOS_DIR
import logging

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        yt_set = set ([found.yt for found in data])
        logger.info(f'videos to download:, {len(yt_set)}')

        for yt in yt_set:
            url = yt.url
            if inputs['fast'] and utils.video_file_exists(yt):
                logger.debug(f'found existing video file for {url}, skipping')
                continue

            logger.debug(f'downloading {url}')
            # YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)

        return data