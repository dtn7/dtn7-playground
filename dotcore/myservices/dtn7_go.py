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
format = "json"

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
