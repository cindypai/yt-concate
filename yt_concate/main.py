import logging

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.download_caption import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.delete_downloaded_file import DeleteDownloadedFile
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.utils import Utils
import sys
import getopt
import logging

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'

def config_logger(logging_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler = logging.FileHandler('yt_concate.log')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def print_usage():
    print('main.py -c <channel_id> -s <search_word> -l <limit>')
    print('main.py '
          '--channel_id <channel_id>'
          '--search_word <search_word>'
          '--limit <number>'
          '--fast<True/False>'
          '--cleanup<True/False>'
          '--logging_level<DEBUG/INFO/WARNING/ERROR/CRITICAL>')
    print('{:>6} {:<12} {}'.format('-c', '--channel_id', 'Channel ID of the Youtube channel to download'))
    print('{:>6} {:<12} {}'.format('-s', '--search_word', 'the word to find in caption'))
    print('{:>6} {:<12} {}'.format('-l', '--limit', 'number of clips'))
    print('{:>6} {:<12} {}'.format('', '--fast', 'skip downloading the existing file'))
    print('{:>6} {:<12} {}'.format('', '--cleanup', 'delete downloaded files when outputs is made'))
    print('{:>6} {:<12} {}'.format('', '--logging_level', 'level to decide whether log show or not'))

def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'fast': True,
        'cleanup': True,
        'logging_level': logging.WARNING,

    }

    short_opts = 'hc:s:l:log:'
    long_opts = 'help channel_id= search_word= limit= fast= cleanup= logging_level='.split()
    print(sys.argv[1:])
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', "--channel_id"):
            inputs['channel_id'] = arg
        elif opt in ('-s', "--search_word"):
            inputs['search_word'] = arg
        elif opt in ('l', '--limit'):
            inputs['limit'] = int(arg)
        elif opt in ('--fast'):
            inputs['fast'] = bool(arg)
        elif opt in ('--cleaup'):
            inputs['cleanup'] = bool(arg)
        elif opt in ('log', '--logging_level'):
            inputs['logging_level'] = eval(f'logging.{arg}')
        print('channel_id is', inputs['channel_id'])
        print('search_word is', inputs['search_word'])
        print('limit is', inputs['limit'])
        print('fast is', inputs['fast'])
        print('cleanup is', inputs['cleanup'])
        print('logging level is', inputs['logging_level'])


    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        DeleteDownloadedFile(),
        Postflight(),

    ]

    config_logger(inputs['logging_level'])
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
