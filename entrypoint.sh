#!/bin/bash

echo "# Starting CORE daemon"
core-daemon > /var/log/core-daemon.log 2>&1 &
sleep 1

# Start CORE gui if $DISPLAY is set
if [ ! -z "$DISPLAY" ]; then
    echo "# Starting CORE gui (DISPLAY=$DISPLAY)"
    core-gui $CORE_PARAMS > /var/log/core-gui.log 2>&1 &
    CORE_GUI_PID=$!

    echo "# Dropping into bash (exit with ^D or \`exit\`)"
    bash

    echo "# Waiting until core-gui is closed..."
    wait $CORE_GUI_PID
else
    echo "# Starting execution of test."
    python3 /root/experiment.py
fi
