CS221 Project (Predicting movie ratings)
========================================
Authors: Carolyn Au (auc@stanford.edu), Justin Cunningham (jcnnghm@stanford.edu), and Weixiong Zheng (zhengwx@stanford.edu)


Code
----

- core libraries:
  - cache.py: Caching layer for our feature extractors
  - config.yaml: Database configuration parameters
  - helpers.py: Utility code to process features and do error analysis
  - movie_filter.py: Generates our test and development movie datasets
  - session.py: Initiates a session with our local copy of the IMDb database
- machine learning tools:
  - feature_creator.py: Generates features using all the feature extractors, outputs data/features.json
  - fann_data_generator.py: Processes data for the neural network
  - scikit_kmeans_runner.py: Generates k-means clusters, outputs new feature files for each cluster configuration
  - sgd_runner.py: Runs linear regression using SGD (modified from class assignment)
  - scikit_learn_runner.py: Runs linear, logistic and SGD regression using scikit
  - fann.py: Runs a neural network using FANN
- analysis tools:
  - pca_analyzer.py: Performs and analyzes the results of PCA
  - feature_analysis.py: Analyzes the distribution of each feature extractor
  - graph.rb: Generates a graph of the neural network
- feature_extractors: Feature extractors and combinators.
- models: Description of the IMDb SQL database tables.
- rotten_tomatoes: Data importer and processor for Rotten Tomatoes movie data.


Setup
-----

You'll want to install all the packages in requirements.txt.

To run the full pipeline, including the feature_creator, you should copy config.yaml.example to config.yaml, and change anything
you need to for your mysql server.


Running the pipeline
--------------------

runner.sh runs the entire pipeline (including reading from the SQL db), first extracting features then each learning algorithm in sequence.
See requirements.txt for python libraries required to run the pipeline.

- python feature_creator.py --verbose
- python scikit_kmeans_runner.py --clusters=10
- python scikit_learn_runner.py --feature-file=data/features_k_means_10.json --save-regularization-stats
- python sgd_runner.py --feature-file=data/features_k_means_10.json
- python fann_data_generator.py --feature-file=data/features_k_means_10.json --postfix="-kmeans-10-pca"
- python fann.py


Data
----

Our complete dataset is available at https://www.dropbox.com/s/wlo1gukdegztvk7/cs221movies.sql.gz?dl=0, and is about 1.4GB compressed.  To use it, you'll need to gunzip it, then import it into a mysql database.  Rename `config.yaml.example` to `config.yaml` and customize that file to point at your database.

For submission, we have a compressed file at data.zip which is the output of our feature_creator.py system on a reduced set of movies.


Example Data and Evaluation Score
---------------------------------

In data.zip, we include the resulting features for all 1977 movies in the test set. Test error
on these movies is 0.72. All predicted rating and actual rating for these
movies are in `example_data_eval_scores.json` for reference.


Adding a feature extractor
--------------------------

Add a new file in the feature_extractors folder containing a class inhering
from Base, implementing the extract method:


    from feature_extractor_base import Base


    class SomeFeatureExtractor(Base):
        __cache__ = False

        def extract(self):
            return {'MOVIE_ID_1': {'my_crazy_feature': 1}}


Registration is automatic, just import your feature extractor in
`feature_extractors/__init__.py`.

    from keywords import SomeFeatureExtractor

You'll probably want to set `__cache__ = False` while you're developing.  When
`__cache__ = True`, the results of extract will be stored in a json file in
the `data/cache` folder, which will prevent feature extractors that you
aren't working on from running.

The feature extractor will have the instance variables `self.session`,
`self.models`, and `self.movie_ids` set.

- `self.session`: A SQLAlchemy session; used for querying the db.
- `self.models`: SQLAlchemy models for each table in the db.
- `self.movie_ids`: An array of all of the movie ids we're using.

In addition, the feature extractor base class provides a few helper
functions:

- `segmented_movie_ids`: this will yield movie_ids in chunks of 500 by default,
  making it a little easier to split up queries.
- `movies_query`: this is just a base query to get all the movies we care about,
  you can string addional stuff onto this.
- `with_appearances`: this can be used to get the number of times a feature
  appears in the dataset, and eliminate features that don't appear enough.

Checkout the `KeywordFeatureExtractor` for a decent example of what the logic
should look like.

By default, FeatureExtractors are included in the baseline, and not exclusive
to the oracle.  To add a feature to the oracle, set `oracle = True` in the
feature extractors class.


Logging
-------
Use the python logging module.

    import logging
    logging.debug("Some log message")

By default, it will log in feature_creator.log.  Set `--verbose` to print
logging messages to stdout.
