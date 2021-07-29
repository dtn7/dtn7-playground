from typing import Tuple

from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode


class Dtn7GoService(CoreService):
    name: str = "dtn7-go"
    group: str = "DTN"
    executables: Tuple[str, ...] = (
        "dtnd",
        "dtn-tool",
    )
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ()
    configs: Tuple[str, ...] = ("dtnd.toml",)
    startup: Tuple[str, ...] = (f'bash -c "nohup dtnd {configs[0]} &> dtnd.log &"',)
    validate: Tuple[str, ...] = ("pgrep dtnd",)
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 1
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ("pkill dtnd",)

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        return f"""
[core]
store = "store_{node.name}"
node-id = "dtn://{node.name}/"
inspect-all-bundles = true

[logging]
level = "debug"
report-caller = false
format = "text"

[discovery]
ipv4 = true
ipv6 = false
interval = 2

[agents]
[agents.webserver]
address = "localhost:8080"
websocket = true
rest = true

[[listen]]
protocol = "mtcp"
endpoint = ":4556"
[routing]
algorithm = "epidemic"
"""


class Dtn7GoSNSensorService(Dtn7GoService):
    name: str = "dtn7-go-sensor"

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        return f"""
[core]
store = "store_{node.name}"
inspect-all-bundles = true
node-id = "dtn://{node.name}.sensor.n40/"

[routing]
algorithm = "epidemic"

[discovery]
ipv4 = true
interval = 2

[agents]
[agents.webserver]
address = "localhost:8080"
websocket = true
rest = true

[[listen]]
protocol = "mtcp"
endpoint = ":4200"
        """


class Dtn7GoSNMuleService(Dtn7GoService):
    name: str = "dtn7-go-mule"

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        return f"""
[core]
store = "store_{node.name}"
inspect-all-bundles = true
node-id = "dtn://{node.name}.mule.n40/"

[routing]
algorithm = "sensor-mule"

[routing.sensor-mule-conf]
sensor-node-regex = "^dtn://[^/]+\\\\.sensor\\\\.n40/.*$"
[routing.sensor-mule-conf.routing]
algorithm = "epidemic"

[discovery]
ipv4 = true
interval = 2

[agents]
[agents.webserver]
address = "localhost:8080"
websocket = true
rest = true

[[listen]]
protocol = "mtcp"
endpoint = ":4200"
        """


class Dtn7GoSNServerService(Dtn7GoService):
    name: str = "dtn7-go-server"

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        return f"""
[core]
store = "store_{node.name}"
inspect-all-bundles = true
node-id = "dtn://{node.name}.server.n40/"

[routing]
algorithm = "epidemic"

[discovery]
ipv4 = true
interval = 2

[agents]
ping = "dtn://{node.name}.server.n40/ping"

[agents.webserver]
address = "localhost:8080"
websocket = true
rest = true

[[listen]]
protocol = "mtcp"
endpoint = ":4200"
        """
