from .corpora import build_corpora
from .preprocess import get_options
from . import basecorpus
import sys, logging
log = logging.getLogger(__name__)

def search(term, corpora):
    """Find all sources that have a given term in them"""
    term = term.upper()
    for corpus in corpora:
        for speaker, content, audio_filename, mfcc in corpus.mfcc_utterances():
            if term in content.upper():
                yield speaker, content, audio_filename, mfcc

def main():
    """Main function for search-and-play of utterances"""
    logging.basicConfig(level=logging.INFO)
    parser = get_options('Search corpora for text and play the matching utterances')
    parser.add_argument(
        'term',
        help='The word/phrase for which to search'
    )
    options = parser.parse_args()
    corpora = build_corpora(options.directory,options.corpus)
    for speaker, content, audio_filename, mfcc in search(options.term, corpora):
        log.info("Playing: %s\n%s", audio_filename,content)
        basecorpus.AudioCorpus.play_audio_file(audio_filename)
