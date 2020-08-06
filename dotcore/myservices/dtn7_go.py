from core.service import CoreService, ServiceMode


class Dtn7GoService(CoreService):
    name = "dtn7-go"

    group = "DTN"

    executables = ("dtnd", "dtn-tool", )

    dependencies = ()

    configs = ("dtnd.toml", )

    startup = ('bash -c "\
nohup dtnd {} &> dtnd_run.log &\
"'.format(configs[0]), )

    validate = ('bash -c "ps -C dtnd"', )       # ps -C returns 0 if the process is found, 1 if not.

    validation_mode = ServiceMode.NON_BLOCKING  # NON_BLOCKING uses the validate commands for validation.

    validation_timer = 1                        # Wait 1 second before validating service.

    validation_period = 1                       # Retry after 1 second if validation was not successful.

    shutdown = ('bash -c "kill -INT `pgrep dtnd`"', )

    @classmethod
    def generate_config(cls, node, filename):
        return '''
[core]
store = "store_{node_name}"
inspect-all-bundles = true
node-id = "dtn://{node_name}/"

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
protocol = "tcpcl"
endpoint = ":4556"
        '''.format(node_name=node.name)


class Dtn7GoSNSensorService(Dtn7GoService):
    name = "dtn7-go-sensor"

    @classmethod
    def generate_config(cls, node, filename):
        return '''
[core]
store = "store_{node_name}"
inspect-all-bundles = true
node-id = "dtn://{node_name}.sensor.n40/"

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
protocol = "tcpcl"
endpoint = ":4556"
        '''.format(node_name=node.name)


class Dtn7GoSNMuleService(Dtn7GoService):
    name = "dtn7-go-mule"

    @classmethod
    def generate_config(cls, node, filename):
        return '''
[core]
store = "store_{node_name}"
inspect-all-bundles = true
node-id = "dtn://{node_name}.mule.n40/"

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
protocol = "tcpcl"
endpoint = ":4556"
        '''.format(node_name=node.name)


class Dtn7GoSNServerService(Dtn7GoService):
    name = "dtn7-go-server"

    @classmethod
    def generate_config(cls, node, filename):
        return '''
[core]
store = "store_{node_name}"
inspect-all-bundles = true
node-id = "dtn://{node_name}.server.n40/"

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
protocol = "tcpcl"
endpoint = ":4556"
        '''.format(node_name=node.name)
