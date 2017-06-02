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


Pulls and pre-processes major Open Source (non-commercial mostly) datasets for spoken audio

* Free software: MIT license
* Documentation: https://audiodatasets.readthedocs.io.
* Supported Datasets:

  * Librispeech (60GB)
  * TEDLIUM_release2 (35GB)
  * VCTK-Corpus (11GB)

* This is intended for use on Linux servers and it is expected that you will be using the 
  library to feed a machine learning system (not necessary, but that's sort of the point of 
  collecting these datasets)

Features
--------

* Downloads common Open Source datasets and performs basic preprocessing on them
* Provides iterables that produce Numpy arrays from the audio data in common formats
* Using `sphfile` directly accesses sph files instead of needing to convert to `wav` first
* Uses a single shared location for the datasets intended to be used by multiple projects

Installation/Setup
------------------

You need to create the download directory and make it writable by the running user. Preferably
you will do that via group-based permissions to allow sharing, but we will here show creation
of a user-specific ownership::

    $ mkdir -p /var/datasets
    $ chown user:group /var/datasets
    $ chmod g+rw /var/datasets

Note that the downloader expects that you have the following available:

    * tar
    * wget

Now you can download the datasets.

.. note:: The datasets are big (100+GB)!

    If you are paying for data or are working on a slow connection you will
    likely want to arrange to do this step during a low-rated period or on a 
    separate data connection.

From a command prompt::

    $ pip install --user audiodatasets
    # this will download 100+GB and then unpack it on disk, it will take a while...
    $ audiodatasets-download 

Creating MFCC data-files::

    # this will generate Multi-frequency Cepestral Coefficient (MFCC) summaries for the 
    # audio datasets (and download them if that hasn't been done)
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
        """Create training, validation and tests datasets"""
        utterances = []
        for corpus in build_corpora():
            utterances.extend( corpus.iter_utterances())
        random.shuffle(utterances)
        train, test,valid = partition( utterances, (3,1,1) )
        def generation( utterances ):
            while True:
                offset = random.randint(0,511)
                for name,transcript,audio_file in utterances:
                    for batch in t.iter_batches( audio_file, batch_size=10, input=input_width, offset=offset ):
                        yield batch,transcript
        return generation(train),generation(test),generation(valid)
