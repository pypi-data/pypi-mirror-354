# F1_lap_time_telementary
This module is created to easily visualize telementary data of the fastest lap from a session. It heavily uses the great FastF1 API below -
https://github.com/theOehrly/Fast-F1/tree/master

This document goes through all available API functions, if you just want a quick way to plot then review the `plot_comparison` function

# Installation
```console
pip install F1-lap-time-telementary
```

# API Functions

## plot_comparison
Creates a telementary for two drivers in any session

### Inputs
year - Year of the race as an integer
gp - The full name of the gp as a string
session_type - Abbreviated session names, mapped as the following:
| session_type    | Session           |
| --------------- | ------------------|
| 'FP1'           | Free Practice 1   |
| 'FP2'           | Free Practice 2   |
| 'FP3'           | Free Practice 3   |
| 'SQ'            | Sprint Qualifying |
| 'SS'            | Sprint Shootout   |
| 'Q'             | Qualifying        |
| 'S'             | Sprint            |
| 'R'             | Race              |

drivers - A list of two drivers with their 3 letter abbreviation. E.g. ['ALO', 'STR']

### Outputs
A matplotlib plot of the telementary data of two drivers
### Usage
```python
from F1_lap_time_telementary import plot_comparison
plot_comparison(
    year=2025,
    grand_prix='Chinese Grand Prix',
    session_type='Q',
    drivers=['ALO', 'STR']
)
```

## setup_plotting
Calls `fastf1.plotting.setup_mpl` from FastF1 to configure the plot
### Inputs
No inputs

### Output
Setup matplotlib for use with fastf1 - Nothing returned from the function

### Usage
```python
from F1_lap_time_telementary import setup_plotting

setup_plotting()
```

## get_session_data
Gets the session data from FastF1

### Inputs
year - Year of the race as an integer
gp - The full name of the gp as a string
session_type - Abbreviated session names, mapped as the following:
| session_type    | Session           |
| --------------- | ------------------|
| 'FP1'           | Free Practice 1   |
| 'FP2'           | Free Practice 2   |
| 'FP3'           | Free Practice 3   |
| 'SQ'            | Sprint Qualifying |
| 'SS'            | Sprint Shootout   |
| 'Q'             | Qualifying        |
| 'S'             | Sprint            |
| 'R'             | Race              |

**Note Sprint Shootout is for 2023 only**

### Outputs
session - Returns a session object

### Usage
```python
from F1_lap_time_telementary import get_session_data

year = 2025
grand_prix = 'Chinese Grand Prix'
session_type='Q'
session = get_session_data(year, grand_prix, session_type)
```

## get_driver_data
Returns the telementary data from the driver's fastest lap

### Inputs
session - A session object (which can be obtained by running `get_session_data`)
driver - Three letter abbreviation for a driver. E.g. 'BOT' for Bottas

### Output
lap - The fastest lap set by the driver in that session
car_data - telementary data from the fastest lap

### Usage
```python
from F1_lap_time_telementary import get_driver_data

session = get_session_data(2025, 'Chinese Grand Prix', 'Q')
driver = 'ALO'
lap, car_data = get_driver_data(session, driver)
```
## get_min_max_speed
Gets the minimum and maximum speed by the driver

### Inputs
car_data - Telementary Data from the car (which can be obtained by running `get_driver_data`)

### Outputs
min_speed - Slowest speed of the car in a lap
max_speed - Top speed of the car in a lap

### Usage
```python
from F1_lap_time_telementary import get_min_max_speed

min_speed, max_speed = get_min_max_speed(car_data)
```
## plot_corners
Plots corner lines in a speed-distance plot

### Inputs
ax - Axes
circuit_data - Circuit Data (Obtained by `session.get_circuit_info`)
car_data - Telementary Data from the car (which can be obtained by running `get_driver_data`)

### Outputs
No output - Adds vertical dashed lines on a speed-distance plot

### Usage
```python
from F1_lap_time_telementary import get_min_max_speed

plot_corners(axs[0], circuit_data, car_data)
```
## plot_telemetry
Plots telementry data 4 subplots -
1) Speed-Distance
2) Throttle-Distance
3) Brake-Distance
4) Gear-Distance

### Inputs
axs - The axes you are plotting on
car_data - Telementary Data from the car (which can be obtained by running `get_driver_data`)
label - The driver's trace that is being plotted

### Outputs
Nothing returned - plots a (4,1) subplot

### Usage
```python
from F1_lap_time_telementary import plot_telemetry
lap, car_data = get_driver_data('Q', 'ALO')
plot_telemetry(axs, car_data, lap)
```

## label_axes
Labels the axes

### Inputs
axs - The axes to label
labels - The y axes labels for the subplots

### Outputs
No output - Axes labelled

### Usage
```python
from F1_lap_time_telementary import label_axes
labels = ['Speed [km/h]', 'Throttle [%]', 'Brake [%]', 'Gear']
label_axes(axs,labels)
```

## add_legends
Adds legend to each subplot

### Inputs
axs - The axes to add legends

### Outputs
No output - Each subplot has a legend

### Usage
```python
from F1_lap_time_telementary import add_legends
add_legends(axs)
```

## set_title
Adds title to the plot

### Inputs
axs - The axes to add a title
title - The title you want to add

### Outputs
No output - Title added to the plot

### Usage
```python
from F1_lap_time_telementary import set_title
set_title(axs, "Qualifying Comparison")
```
