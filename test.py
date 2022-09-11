from flightFare.config.configuration import Configuartion
from flightFare.pipeline.pipeline import Pipeline

pipeline = Pipeline(config=Configuartion())
pipeline.run_pipeline()