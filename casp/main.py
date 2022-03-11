import yaml
import types
import typing
import casp.module as modules

from abc import ABC, abstractmethod


class PipelineStrategy(ABC):
    """ETL Strategy"""

    @abstractmethod
    def run(self, config: dict, pipeline: object):
        pass


class ExtractPipeline(PipelineStrategy):
    """Executes extract step of pipeline"""

    def run(self, config: dict, pipeline: object):
        return pipeline.extract(**config.get("extract") or {})


class TransformPipeline(ExtractPipeline):
    """Executes transform step of pipeline"""

    def run(self, config: dict, pipeline: object):
        extract = super().run(config, pipeline)
        return pipeline.transform(extract, **config.get("transform") or {})


class LoadPipeline(TransformPipeline):
    """Executes load step of pipeline"""

    def run(self, config: dict, pipeline: object):
        transform = super().run(config, pipeline)
        return pipeline.load(transform, **config.get("load") or {})


class RunPipeline(LoadPipeline):
    """Executes all pipeline steps"""

    def run(self, config: dict, pipeline: object):
        load = super().run(config, pipeline)
        return load


class CLI:
    """Command line interface class that runs multiple strategies"""

    def __init__(self, config) -> None:
        """Adds the run configuration file"""
        self.config = self.load_config(config)

    def execute_etl(self, strategy: PipelineStrategy):
        """Executes the given strategy"""
        name = self.config.get("name")
        pipeline_order = self.config.get("order")

        print(f"Starting pipeline: {name}")
        for id, pipeline_config in pipeline_order.items():
            print(f"Running pipeline: {id}")    #: TODO - Add logging
            strategy.run(pipeline_config, self.get_pipeline_instance(pipeline_config))

    def get_pipeline_instance(self, config: dict) -> object:
        """Creates a pipeline instance from configuration"""
        return self.get_instance(modules, "module", config)

    def load_config(self, filename: str) -> dict:
        """Load a configuration file as YAML."""
        with open(filename) as fh:
            config = yaml.safe_load(fh)

        return config

    def get_instance(
        self, module: types.ModuleType, name: str, config: typing.Any, *args: typing.Any
    ) -> typing.Any:
        """Helper to construct an instance of a class."""
        ctor_name = config[name].get("type")

        if ctor_name == None:
            return None

        return getattr(module, ctor_name)(*args, **config[name].get("args"))