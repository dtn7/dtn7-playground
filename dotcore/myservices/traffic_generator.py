from core.services.coreservices import CoreService


class TrafficGeneratorService(CoreService):
    name = "TrafficGenerator"
    group = "DTN"
    executables = ("traffic_generator.py",)
    dependencies = ("dtn7-go",)

    @classmethod
    def get_startup(cls, node):
        return ('bash -c "nohup traffic_generator.py &> traffic_generator_run.log &"',)
