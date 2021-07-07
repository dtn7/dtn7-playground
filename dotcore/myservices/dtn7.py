from core.services.coreservices import CoreService, ServiceMode

class Dtn7Service(CoreService):
    name = "DTN7"
    group = "dtn"
    executables = ("dtnd", "dtn-tool")
    dependencies = ()
    configs = ("dtnd.toml",)
    startup = (f'bash -c "nohup dtnd {configs[0]} &> dtnd_run.log &"',)
    validation_timer = 1  # Wait 1 second before validating service.
    validation_period = 1  # Retry after 1 second if validation was not successful.
    validation_mode = ServiceMode.NON_BLOCKING  # NON_BLOCKING uses the validate commands for validation.
    shutdown = ('bash -c "kill -INT `pgrep dtnd`"',)
    validate = ('bash -c "ps -C dtnd"',)  # ps -C returns 0 if the process is found, 1 if not.

    @classmethod
    def generate_config(cls, node, filename):
        if filename == "dtnd.toml":
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
        else:
            return ""