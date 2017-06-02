"""Download and convert 3 major data-sets for voice dictation

LibriSpeech, TEDLIUM_release2 and VCTK

The 3 Data-sets here required around 100GB of downloads, so
the idea of this module is that you'll download the dataset 
once and then use it for many experiments.
"""
import os
import numpy
import logging
import librosa.core
import librosa.feature
import soundfile
import sounddevice
log = logging.getLogger(__name__)
DEFAULT_DATASET_DIR = '/var/datasets'


class AudioCorpus(object):
    """Pulls, unpacks and pre-processes large spoken-word datasets"""
    STORE_IN_SUBDIR = False
    LOCAL_DIR = 'UNSPECIFIED'
    DOWNLOAD_SIZES = {
        #'filename':int,
    }
    DOWNLOAD_URL = 'https://example.com/'
    DOWNLOAD_FILES = [
        #'basefilename.tar.gz'
    ]
    UNPACKED_FLAGS = [
        #'path/to/file/that/indicates/unpacked/state.wav'
    ]

    def __init__(self, dataset_dir=DEFAULT_DATASET_DIR):
        self.dataset_dir = dataset_dir

    @property
    def local_dir(self):
        """Property providing our local data/storage directory"""
        return os.path.join(self.dataset_dir, self.LOCAL_DIR)

    def download_filename(self, filename):
        """Combine filename with our directory to determine final download location"""
        if self.STORE_IN_SUBDIR:
            expected_filename = os.path.join(self.local_dir, filename)
        else:
            expected_filename = os.path.join(self.dataset_dir, filename)
        return expected_filename

    def to_download(self):
        """Produce the set of things we would like to download"""
        for filename in self.DOWNLOAD_FILES:
            expected_filename = self.download_filename(filename)
            expected_size = self.DOWNLOAD_SIZES.get(filename)
            formatted_size = expected_size // (1024 * 1024)
            if not os.path.exists(expected_filename):
                log.info("Need to download file %s (%sMiB)",
                         filename, formatted_size)
                yield {
                    'url': self.DOWNLOAD_URL + filename, 'filename': expected_filename,
                    'expected_size': expected_size,
                }
            else:
                size = os.stat(expected_filename).st_size
                if size != expected_size:
                    log.info(
                        "Unfinished download on %s (%s%% of %sMiB)",
                        expected_filename,
                        round((size / expected_size) * 100, 1),
                        formatted_size,
                    )
                    yield {
                        'url': self.DOWNLOAD_URL + filename,
                        'filename': expected_filename,
                        'expected_size': expected_size,
                        'start': size
                    }
                else:
                    log.info("%s finished download", expected_filename)

    def to_unpack(self):
        """Produce the set of things we would like to unpack"""
        for download, flag in zip(self.DOWNLOAD_FILES, self.UNPACKED_FLAGS):
            download_filename = self.download_filename(download)
            expected_filename = os.path.join(self.local_dir, flag)
            if not os.path.exists(expected_filename):
                if os.path.exists(download_filename):
                    log.info("Need to unpack: %s", download_filename)
                    yield {
                        'filename': download_filename,
                        'flag': expected_filename,
                    }
                else:
                    log.warn("Seem to be missing %s file cannot unpack",
                             download_filename)
            else:
                log.info("%s finished unpacking", download_filename)

    @classmethod
    def load_audio_file(cls, audio_filename):
        """Load given audio-file into a numpy array @16kHz"""
        if audio_filename.endswith('.wav'):
            audio, sr = librosa.load(
                audio_filename,
                mono=True,
                sr=None
            )
        else:
            # .flac files mostly
            audio, sr = soundfile.read(audio_filename)
        if sr != 16000:
            audio = librosa.core.resample(
                audio, sr, 16000,
            )
        return audio

    def iter_batches(self, audio_filename, batch_size=10, input=64, offset=0):
        """Iterate set of batches from audio_filename

        returns iterator of array[batch_size:1:input] of
        16KHz raw audio samples
        """
        matrix = self.load_audio_file(audio_filename)
        slice_size = batch_size * input
        blocks = (len(matrix) - offset) // slice_size
        for i in range(blocks):
            batch = matrix[
                offset + i *slice_size:offset + (i + 1) * slice_size
            ]
            yield batch.reshape((batch_size, 1, input))

    @classmethod
    def play_audio_file(cls, audio_filename):
        """Play an audio file from disk for quality checks"""
        content = cls.load_audio_file(audio_filename)
        sounddevice.play(content, 16000, blocking=True)

    def iter_utterances(self):
        """Produce iterator yielding (speakerid,transcript,audio_filename)"""
        raise NotImplementedError

    def mfcc_utterances(self):
        """Iterate speaker, content, audio_filename, mfcc_filename for this dataset"""
        for speaker, content, audio_filename in self.iter_utterances():
            expected = audio_filename + '.mfcc.npy'
            if not os.path.exists(expected):
                log.info("Extracting MFCC from %s", audio_filename)
                audio = self.load_audio_file(audio_filename)
                mfcc = librosa.feature.mfcc(audio, sr=16000)
                if len(content) < mfcc.shape[1]:
                    # save mfcc
                    numpy.save(expected, mfcc, allow_pickle=False)
                else:
                    log.warn(
                        "Skipping %s as MFCC is fewer samples than transcript", audio_filename)
                    continue
            yield speaker, content, audio_filename, expected
