from core.service import CoreService
from core.service import ServiceMode


class BWMService(CoreService):
    name = "bwm-ng"

    group = "Logging"

    executables = ('bwm-ng', )

    startup = ('bash -c "\
nohup bwm-ng --timeout=1000 --unit=bytes --type=rate --output=csv -F bwm.csv &> bwm_run.log &\
"', )

    validate = ('bash -c "ps -C bwm-ng"', )     # ps -C returns 0 if the process is found, 1 if not.

    validation_mode = ServiceMode.NON_BLOCKING  # NON_BLOCKING uses the validate commands for validation.

    validation_timer = 1                        # Wait 1 second before validating service.

    validation_period = 1                       # Retry after 1 second if validation was not successful.

    shutdown = ('bash -c "kill -INT `pgrep bwm-ng`"', )
