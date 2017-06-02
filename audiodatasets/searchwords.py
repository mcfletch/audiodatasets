from . import preprocess
import sys

def search( term, corpora=None ):
    """Find all sources that have a given term in them"""
    term = term.upper()
    if corpora is None:
        corpora = preprocess.build_corpora()
    for corpus in corpora:
        for speaker, content, audio_filename, mfcc in corpus.mfcc_utterances():
            if term in content.upper():
                yield speaker, content, audio_filename, mfcc

if __name__ == "__main__":
    for speaker,content,audio_filename,mfcc in search( sys.argv[1] ):
        print("%s"%( content,))
        preprocess.AudioCorpus.play_audio_file( audio_filename )

