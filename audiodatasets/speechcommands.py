import os
import glob

from . import basecorpus


class SpeechCommands(basecorpus.AudioCorpus):
    """Tensorflow speech commands dataset"""
    CURRENT = 'speech_commands_v0.01.tar.gz'
    DOWNLOAD_SIZES = {
        CURRENT : 1488293908,
    }
    DOWNLOAD_URL = 'http://download.tensorflow.org/data/'
    DOWNLOAD_FILES = [
        CURRENT
    ]
    LOCAL_DIR = 'speech-commands'
    UNPACKED_FLAGS = [
        'zero/004ae714_nohash_0.wav',
    ]

    def iter_utterances(self):
        """Produce iterable with speaker_id, utterance_text, audio_filename

        Note that the wav-files in VCTK are 48kHz instead of 16kHz,
        so they need to be down-sampled to match the rest of the datasets
        """
        filenames = sorted(glob.glob(
            os.path.join(self.local_dir,'*','*')
        ))
        


CORPUS = SpeechCommands
