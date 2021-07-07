import os

from core.services.coreservices import CoreService

class TrafficGeneratorService(CoreService):
    name = "TrafficGenerator"
    group = "dtn"
    executables = ("/utils/traffic_generator.py",)
    dependencies = ("DTN7",)

    @classmethod
    def get_startup(cls, node):
        name = node.name
        number_of_bundles = os.environ['BUNDLES_PER_NODE']
        payload_size = os.environ['PAYLOAD_SIZE']
        runtime = os.environ['EXPERIMENT_RUNTIME']
        return (f'bash -c "nohup python3 /utils/traffic_generator.py {name} {payload_size} {number_of_bundles} {runtime} &> traffic_generator_run.log &"',)

