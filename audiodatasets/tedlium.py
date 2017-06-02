import os
import glob
from . import basecorpus
import sphfile
import logging
log = logging.getLogger(__name__)


class TEDLIUM2(basecorpus.AudioCorpus):
    DOWNLOAD_SIZES = {
        'TEDLIUM_release2.tar.gz': 36791529840
    }
    DOWNLOAD_URL = 'http://www.openslr.org/resources/19/'
    DOWNLOAD_FILES = [
        'TEDLIUM_release2.tar.gz',
    ]
    LOCAL_DIR = 'TEDLIUM_release2'
    UNPACKED_FLAGS = [
        'train/sph/ZeresenayAlemseged_2007G.sph',
    ]

    def iter_utterances(self):
        """Produce iterable with speaker_id, utterance_text, audio_filename

        TEDLIUM2 files are .sph files, we use sphfile to convert to 
        wav-files, other than some files being big-endian the formats are 
        1-channel 16-bit 16kHz
        """
        for subset in ['dev', 'test', 'train']:
            for transcript in glob.glob(os.path.join(self.local_dir, subset, 'stm', '*.stm')):
                base = os.path.splitext(os.path.basename(transcript))[0]
                sph_filename = os.path.join(
                    self.local_dir, subset, 'sph', base + '.sph'
                )
                audio = sphfile.SPHFile(sph_filename)
                for i, line in enumerate(open(transcript).read().splitlines()):
                    line = line.split(' ', 6)
                    filename, _, speaker, start, stop, meta, content = line
                    if speaker == 'inter_segment_gap':
                        continue
                    wav_file = os.path.join(
                        os.path.dirname(sph_filename),
                        '%s_%04i.wav' % (speaker, i)
                    )
                    if not os.path.exists(wav_file):
                        log.info("Extracting sph audio to %s", wav_file)
                        audio.write_wav(wav_file, float(start), float(stop))
                    yield filename, content, wav_file
#                for key,expected in (('channel_count',1),('sample_n_bytes',2),('sample_rate',16000)):
#                    real = audio.format[key]
#                    if real != expected:
#                        log.warn("File %s doesn't have expected %s is %s instead of %s",
#                            sph_filename, real, expected )


CORPUS = TEDLIUM2
