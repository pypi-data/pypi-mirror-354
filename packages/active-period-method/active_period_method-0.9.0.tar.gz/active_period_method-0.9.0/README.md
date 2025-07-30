# Active Period Method
Detecting bottlenecks in production environments via the Active Period Method is computationally expensive and requires
specific algorithms.
The purpose of this package is to give a user-friendly package to compute shifting bottlenecks from production event data.

![momentary-bottlenecks.svg](docs%2Fmomentary-bottlenecks.svg)

## Getting Started
Install the python module via:
```
pip install active_period_method
```
Once installed, the module can be used via the ```detect_bottlenecks``` method:
```
from active_period_method import detect_bottlenecks

momentary_bottlenecks, average_bottlenecks = detect_bottlenecks(df)
```
The method differentiates between **momentary** bottlenecks which can be plotted as a station Gantt (as shown above) and
**average** bottlenecks which aggregates bottleneck states along the total active time of the station.

## Theoretical Approach
In context of this project a bottleneck is a resource that limits the throughput of the entire production system.
The Active Period Method for bottleneck detection in manufacturing was first developed by 
[Roser et al. (2002)](https://ieeexplore.ieee.org/document/1166360) and works under the assumption that at any given time
the station with the longest uninterrupted active duration can be considered a bottleneck.
Therefore, a momentary bottleneck can be described as the timespan during which a station
can be considered a bottleneck for the production system.
Unlike many other data driven bottleneck detection methods, the Active Period Method does not require any knowledge
about the material flow in the production system, since it only takes station states into account.
Thanks to its temporal resolution Active Period Method differentiates between a resource being the sole bottleneck at a
given time and a bottleneck "shifting" between multiple resources at any given moment.
A bottleneck is considered to be shifting if multiple temporary longest active periods overlap at a given moment.
This differentiation allows for a more granular analysis of bottlenecks in the production system.

Remark:
Since the Active Period Method is a data driven bottleneck detection method it can only analyse bottlenecks "post mortem".
It detects bottlenecks in the past, depending on recorded station states. The method does not give any indication 
about future situations or the effects of alleviating a detected bottleneck.

## How to Use
### Prerequisites
The Active Period Method requires the given event DataFrame to include at least a column for timestamp, station and status.
An example for the required data format can be found below:

| station  |      timestamp      | status |
|:---------|:-------------------:|-------:|
| Station1 | 01-01-2025 08:00:00 |   True |
| Station2 | 01-01-2025 08:02:03 |   True |
| Station3 | 01-01-2025 08:34:07 |   True |
| Station1 | 01-01-2025 09:12:35 |  False |
| ...      |         ...         |    ... |

The station name should be the stations id as a string or number, the timestamp must be of the data type **pd.Datetime** and
the status must be a **boolean** value to indicate the active state.

Remark:
The status used in the input data only differentiates between events which show an active state of the respective stations and
events which set the stations state to inactive. Depending on your data it might be necessary to evaluate your specific status 
events as either active or inactive beforehand.

### Bottleneck Detection
The Active Period Method differentiates between momentary bottlenecks which can be plotted as a station Gantt (as shown above) and
average bottlenecks which cumulates the total momentary bottleneck duration divided by the total active time of the respective station.
Detecting bottlenecks can be done either by using the wrapper method, as described [above](#getting-started) or by instantiating the 
```ActivePeriodMethod``` class:
```
from active_period_method import ActivePeriodMethod

active_period_method = ActivePeriodMethod(df)
momentary_bottlenecks = active_period_method.calculate_momentary_bottlenecks()
average_bottlenecks = active_period_method.calculate_average_bottlenecks()
```
Keep in mind that momentary bottlenecks must be calculated <u>before</u> average bottlenecks since average bottlenecks
are an aggregation of the momentary bottleneck states.

### Plotting
The Active Period Method module support plotting both the ```detect_bottlenecks``` method and 
the ```ActivePeriodMethod``` class support plotting of the detected 
bottlenecks by either using ```matplotlib``` or ```plotly.express```.

Detected momentary bottlenecks can be plotted in a station Gantt chart. 
This can be done via the ```visualize_momentary_bottlenecks()``` method of an ```ActivePeriodMethod``` object.

Average bottlenecks may also be plotted as an aggregated barchart, differentiating between sole and shifting bottleneck phases.
Use the ```visualize_average_bottlenecks()``` method of an ```ActivePeriodMethod``` object to achieve this.

![average-bottlenecks.svg](docs%2Faverage-bottlenecks.svg)

### Interpretation
The detected momentary bottlenecks indicate during which recorded period a station was considered a bottleneck. 
For average bottleneck calculation, the total shifting and sole bottleneck durations of a stations are cumulated and 
divided by the total time the station was recorded active. This can lead to the false assumption that the average 
sole bottleneck ratios should sum to 1. This is not the case.
The bottleneck ratio of a station is merely an indicator of the severity of a station's bottleneck and
should therefore be treated as a starting point for further analysis and improvement initiatives.

## Development
This implementation of the Active Period Method was developed in the context of the 
DAWOPT (DAtenstrom zur WertstromOPTimierung) research project by iFAKT GmbH and Fraunhofer IPA 
funded by the Invest BW program of the Ministry of Economic Affairs, Labor and Tourism Baden-Württemberg.

### Participate
If you would like to participate in the development of this project please feel free to do so.
We provide guidelines for code formatting in the [pyproject.toml](pyproject.toml) file.

### Testing
The Active Period Method project's code supports multiple tests driven by the ```pytest``` testing framework.
If you would like to participate in further development of this project, please consider using (and/or extending)
the given test suite. We provide further information about test cases in the [tests.md](tests%2Ftests.md) file.

### Project Organisation
```
active-period-method
├──README.md
├──pyproject.toml
├──gitlab-ci.yml
├──requirements.txt
├──src
|   └──active_period_method
|       ├──__init__.py
|       ├──acitve_period_method.py
|       ├──detect_bottlenckes.py
|       ├──machine.py
|       └──utils
├──tests
|   └──data
└──docs
```

## License

This project is licensed under the [MIT License](LICENSE.txt).

© 2025 Martin Jestädt, Marco Bernreuther, Benjamin Epple

