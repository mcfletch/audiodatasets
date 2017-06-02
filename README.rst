==============
Audio Datasets
==============


.. image:: https://img.shields.io/pypi/v/audiodatasets.svg
        :target: https://pypi.python.org/pypi/audiodatasets

.. image:: https://img.shields.io/travis/mcfletch/audiodatasets.svg
        :target: https://travis-ci.org/mcfletch/audiodatasets

.. image:: https://readthedocs.org/projects/audiodatasets/badge/?version=latest
        :target: https://audiodatasets.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mcfletch/audiodatasets/shield.svg
     :target: https://pyup.io/repos/github/mcfletch/audiodatasets/
     :alt: Updates


Pulls and pre-processes major Open Source datasets for spoken audio

* Supported Datasets:

  * `Librispeech <http://www.openslr.org/resources/12/>`_ (60GB)
  * `TEDLIUM_release2 <http://www.openslr.org/resources/19/>`_ (35GB)
  * `VCTK-Corpus <http://homepages.inf.ed.ac.uk/jyamagis/release/>`_ (11GB)

* This is intended for use on Linux servers and it is expected that you will be using the 
  library to feed a machine learning system (not necessary, but that's sort of the point of 
  collecting these datasets)
* MIT license for the software, but please note that the datasets themselves are 
  generally for non-commercial use only

Features
--------

* Downloads common Open Source datasets and performs basic preprocessing on them
* Provides iterables that produce Numpy arrays from the audio data in common formats
* Uses `sphfile` to directly accesses sph files instead of needing to convert to `wav` first
* Uses a single shared location for the datasets intended to be used by multiple projects

Installation/Setup
------------------

You need to create the download directory and make it writable by the running user. Preferably
you will do that via group-based permissions to allow sharing, but we will here show creation
of a user-specific ownership::

    $ mkdir -p /var/datasets
    $ chown user:group /var/datasets
    $ chmod g+rw /var/datasets

if `/var/datasets` doesn't exist, or isn't writable, the downloader will instead populate
`~/.config/datasets` with the data. You may wish to link that directory to `/var/datasets`
so that you can use default instantiations of the corpora::

    $ ln -s /var/datasets ~/.config/datasets

Note that the downloader expects that you have the following available, this may not
yet be the case in a docker or minimal OS installation:

    * `tar`
    * `wget`

Now you can download the datasets.

.. note::

    The datasets are big (100+GB)!
    
    If you are paying for data or are working on a slow connection you will
    likely want to arrange to do this step during a low-rated period or on a 
    separate data connection.

From a command prompt::

    $ pip install audiodatasets
    # this will download 100+GB and then unpack it on disk, it will take a while...
    $ audiodatasets-download 

Creating MFCC data-files::

    # this will generate Multi-frequency Cepestral Coefficient (MFCC) summaries for the 
    # audio datasets (and download them if that hasn't been done). This isn't necessary
    # if you are doing only raw-audio processing
    $ audiodatasets-preprocess 

Playing some audio::

    # this will iterate through playing every utterance that includes 'moon' in the transcript
    $ audiodatasets-search 'moon'

Usage
-------

Once setup, you likely want to iterate over the data-sets using, for instance, a partition to 
separate out test/train/validate data. To iterate over the raw audio:

.. code:: python

    from audiodatasets.corpora import build_corpora, partition
    import random

    def train_valid_test():
        """Create training, validation and tests datasets
        
        returns three iterators yielding (array[10:512],transcript) batches
        """
        utterances = []
        for corpus in build_corpora():
            utterances.extend( corpus.iter_utterances())
        random.shuffle(utterances)
        train, test,valid = partition( utterances, (3,1,1) )
        def generation( utterances ):
            while True:
                offset = random.randint(0,511)
                for name,transcript,audio_file in utterances:
                    for batch in t.iter_batches( audio_file, batch_size=10, input=512, offset=offset ):
                        yield batch,transcript
        return generation(train),generation(test),generation(valid)

To iterate over the 10ms MFCC preprocessed data, which yields 20 frequency batches per 
processing window (10ms):

.. code:: python

    from audiodatasets.corpora import build_corpora, partition
    import random

    def train_valid_test():
        """Create training, validation and tests datasets

        Note: the batches vary in *time* at highest frequency, while
        the frequency bins are the second-highest frequency.

        See: `LibRosa MFCC <https://librosa.github.io/librosa/generated/librosa.feature.mfcc.html>`_
        
        returns three iterators yielding (array[10:20:63],transcript) batches
        """
        utterances = []
        for corpus in build_corpora():
            utterances.extend( corpus.mfcc_utterances())
        random.shuffle(utterances)
        train, test,valid = partition( utterances, (3,1,1) )
        def generation( utterances ):
            while True:
                offset = random.randint(0,62)
                for name,transcript,audio_file in utterances:
                    for batch in t.iter_batches( audio_file, batch_size=10, input=63, offset=offset ):
                        yield batch,transcript
        return generation(train),generation(test),generation(valid)
