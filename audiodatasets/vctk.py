import os
import glob

from . import basecorpus


class VCTK(basecorpus.AudioCorpus):
    """Voice Cloning Toolkit"""
    DOWNLOAD_SIZES = {
        'VCTK-Corpus.tar.gz': 11159466829,
    }
    DOWNLOAD_URL = 'http://homepages.inf.ed.ac.uk/jyamagis/release/'
    DOWNLOAD_FILES = [
        'VCTK-Corpus.tar.gz'
    ]
    LOCAL_DIR = 'VCTK-Corpus'
    UNPACKED_FLAGS = [
        'wav48/p376/p376_295.wav'  # just a random file...
    ]

    def iter_utterances(self):
        """Produce iterable with speaker_id, utterance_text, audio_filename

        Note that the wav-files in VCTK are 48kHz instead of 16kHz,
        so they need to be down-sampled to match the rest of the datasets
        """
        speakers = [int(speaker[0]) for speaker in open(
            os.path.join(self.local_dir, 'speaker-info.txt')
        ).read().splitlines()[1:]]
        for speaker in speakers:
            utterances = glob.glob(os.path.join(
                self.local_dir, 'txt/p%s/p%s_*.txt' % (speaker, speaker),
            ))
            for utterance in utterances:
                utterance_id = int(
                    os.path.splitext(os.path.basename(utterance))[
                        0].split('_')[1]
                )
                content = open(utterance).read()
                # TODO: these are still 48kHz, we need 16kHz
                yield 'VCTK-%s' % speaker, content, os.path.join(
                    self.local_dir,
                    'wav48/p%(speaker)s/p%(speaker)s_%(utterance)s.wav' % locals()
                )


CORPUS = VCTK
