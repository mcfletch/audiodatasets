"""Calculate various statistics for the MFCC preprocessed data"""
from . import corpora
from .baseoptions import get_options
import logging
log = logging.getLogger(__name__)

class Stat(object):
    def __init__(self,name):
        self.name = name
        self.min = 2**31-1
        self.max = 0
        self.total = 0
        self.count = 0
    def show(self):
        log.info(
            "%s:\n  Min: %s:\n  Max:%s\n  Mean:%s",
            self.name,
            self.total/float(self.count or 1),
            self.min,
            self.max,
        )
    def add(self, value):
        if value > self.max:
            self.max = value 
        if value < self.min:
            self.min = value 
        self.total += value 
        self.count += 1

def main():
    logging.basicConfig(level=logging.INFO)
    parser = get_options('Extract some basic stats for mfcc dataset')
    options = parser.parse_args()
    mfcc = Stat('MFCC Length')
    trans = Stat('Transcription Length')
    for corpus in corpora.build_corpora(options.directory, options.corpus):
        for record in corpus.mfcc_utterances():
            transcript = record[1]
            filename = record[-1]
            array = corpus.load_mfcc_file( filename )
            alen = array.shape[-1]
            mfcc.add( alen )
            trans.add( len(transcript))
    mfcc.show()
    trans.show()
    log.info("%s Utterances",transcript.count)
