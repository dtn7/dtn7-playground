# Github Actions test framework for DTN7-Go

This branch aims to give a framework for extended DTN7-Go testing using the
[CORE emulator](http://github.com/coreemu/core) and Github Actions.

### Structure
The `dotcore` folder holds all configurations required for CORE.
`dotcore/configs` holds all XML and IMN files to describe a scenario.
`dotcore/myservice` contains the service for starting a DTN7-Go node together
with a traffic generator, i.e., a small program to generate and send bundles
periodically. `dotcore/experiments` holds the experiment Python script for a
particular experiment. The `bin` folder holds the traffic generator itself,
which is started by the traffic generator CORE service. Finally,
`.github/workflows` defines the experiments and step to be executed for a given
experiment.

### How to install own tests
To install a new experiment, you have to define a scenario using Cores XML
export and place it using a meaningful name in the `dotcore/configs` folder.
After that, write your experiment using Cores Python API and store it with a
meaningful name in `dotcore/experiments`. If you have to use custom Core
Services, you have to write them yourself and place them accordingly in the
`dotcore/myservices` folder. Finally, define the steps for the test either in a
new workflow YAML file or in the existing on a as new job and place it in the
`.github/workflow` folder.

### Existing Experiments
DTN7-Go tends to deadlock after some time, making it impossible to send any
bundles. Therefore, the `Run CORE experiments` jobs defines 30 CORE nodes that
are more or less connected randomly and sending a different number of files with
various sizes over a time period. The main experiment script is the
`dotcore/experiments/deadlock.py` Python file, which starts the
`dotcore/configs/deadlock.xml` scenario. The corresponding Github Workflow is
called `Deadlock Experiment Testing` in the `.github/workflows/core.yml` file.
