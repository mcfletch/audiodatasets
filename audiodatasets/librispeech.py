"""Download and convert 3 major data-sets for voice dictation

LibriSpeech, TEDLIUM_release2 and VCTK

The 3 Data-sets here required around 100GB of downloads, so
the idea of this module is that you'll download the dataset 
once and then use it for many experiments.
"""
import os
import glob
import logging
log = logging.getLogger(__name__)
from . import basecorpus


class LibriSpeech(basecorpus.AudioCorpus):
    DOWNLOAD_SIZES = {
        'dev-clean.tar.gz': 337926286,
        'dev-other.tar.gz': 314305928,
        'intro-disclaimers.tar.gz': 695964615,
        'test-clean.tar.gz': 346663984,
        'test-other.tar.gz': 7340032,
        'train-clean-100.tar.gz': 6387309499,
        'train-clean-360.tar.gz': 23049477885,
        'train-other-500.tar.gz': 30593501606,
    }
    DOWNLOAD_URL = 'http://www.openslr.org/resources/12/'
    STORE_IN_SUBDIR = True
    DOWNLOAD_FILES = [
        'dev-clean.tar.gz',
        'dev-other.tar.gz',
        'test-other.tar.gz',
        'test-clean.tar.gz',
        'intro-disclaimers.tar.gz',
        'train-clean-100.tar.gz',
        'train-clean-360.tar.gz',
        'train-other-500.tar.gz',
    ]
    UNPACKED_FLAGS = [
        'dev-clean',
        'dev-other',
        'test-other',
        'test-clean',
        'intro',
        'train-clean-100',
        'train-clean-360',
        'train-other-500',
    ]
    LOCAL_DIR = 'LibriSpeech'

    def iter_utterances(self, categories=None):
        """Produce iterable with speaker_id, utterance_text, audio_filename

        LibriSpeech files are already in our preferred format
        """
        if categories is None:
            categories = self.UNPACKED_FLAGS
        else:
            categories = categories
        for category in categories:
            for translation in glob.glob(os.path.join(self.local_dir, category, '*/*/*.txt')):
                directory = os.path.dirname(translation)
                for line in open(translation).read().splitlines():
                    try:
                        id, content = line.split(' ', 1)
                    except ValueError:
                        log.error(
                            "Unexpected translation line format: %r", line)
                    speaker, chapter, utterance = id.split('-')
                    flac_file = os.path.join(directory, '%s.flac' % (id,))
                    yield 'Libri-%s-%s' % (category, int(speaker)), content, flac_file


CORPUS = LibriSpeech
