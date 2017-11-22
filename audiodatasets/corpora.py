"""Get a set of corpora for a given directory"""
import os
from .settings import PERSONAL_DATASET_DIR

def build_corpora(target=PERSONAL_DATASET_DIR, corpora=None):
    """Build corpora for given target

    target -- DIRNAME in which dataset is stored
    corpora -- None or subset of ['tedlium','vctk','librispeech']

    returns list of `basecorpus.AudioCorpus` instances
    """
    from . import tedlium
    from . import vctk
    from . import librispeech
    from . import speechcommands
    target = os.path.expanduser(target)
    all_corpora = {
        'tedlium': tedlium.CORPUS,
        'vctk': vctk.CORPUS,
        'librispeech': librispeech.CORPUS,
        'librespeech': librispeech.CORPUS,
        'speechcommands': speechcommands.CORPUS,
    }
    if not corpora:
        corpora = all_corpora.values()
    else:
        corpora = [(all_corpora[c] if c in all_corpora else c)
                   for c in corpora]
    return [cls(target) for cls in corpora]

def partition(data, fragments):
    """Partion list into relative fractions"""
    total = sum(fragments)
    relative = len(data) // total
    i = 0
    for fragment in fragments:
        yield data[i:i+fragment*relative]
