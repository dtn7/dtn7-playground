from core.service import CoreService, ServiceMode


class Dtn7Service(CoreService):
    name = "DTN7"

    group = "DTN"

    executables = ("dtn7d", "dtn7cat", )

    dependencies = ("bwm-ng", "pidstat")

    configs = ("dtn7d.toml", )

    startup = ('bash -c "\
nohup dtn7d {} &> dtn7d_run.log &\
"'.format(configs[0]), )

    validate = ('bash -c "ps -C dtn7d"', )      # ps -C returns 0 if the process is found, 1 if not.

    validation_mode = ServiceMode.NON_BLOCKING  # NON_BLOCKING uses the validate commands for validation.

    validation_timer = 1                        # Wait 1 second before validating service.

    validation_period = 1                       # Retry after 1 second if validation was not successful.

    shutdown = ('bash -c "kill -INT `pgrep dtn7d`"', )

    @classmethod
    def generate_config(cls, node, filename):
        return '''
[core]
store = "store_{node_name}"
node-id = "dtn://{node_name}/"

# [logging]
# level = "debug"
# report-caller = false
# format = "json"

[routing]
algorithm = "epidemic"

[discovery]
ipv4 = true
interval = 2

[simple-rest]
node = "dtn://{node_name}/"
listen = "127.0.0.1:8080"

[[listen]]
protocol = "mtcp"
endpoint = ":1312"
        '''.format(node_name=node.name)
