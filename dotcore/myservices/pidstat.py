from core.service import CoreService
from core.service import ServiceMode


class PidstatService(CoreService):
    name = "pidstat"

    group = "Logging"

    executables = ('pidstat', )

    startup = ('bash -c "\
nohup pidstat -drush -p ALL 1 > pidstat.log 2> pidstat_run.log &\
"', )

    validate = ('bash -c "ps -C pidstat"', )     # ps -C returns 0 if the process is found, 1 if not.

    validation_mode = ServiceMode.NON_BLOCKING  # NON_BLOCKING uses the validate commands for validation.

    validation_timer = 1                        # Wait 1 second before validating service.

    validation_period = 1                       # Retry after 1 second if validation was not successful.

    shutdown = ('bash -c "kill -INT `pgrep pidstat`"', )
