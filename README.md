# QUALITY IMAGING TIME CALCULATOR

Python script to display the Quality Imaging Hours on a given date.

## Quality Imaging Hours

Quality Imaging Time is a concept developed by [Charles Bracken](https://digitalstars.wordpress.com/). In order to take astrophotographs a dark sky is needed. Astronomically, it means the Sun must be well below the horizon, the Moon shouldn't interfer too much (ideally, it should be also below the horizon) and the imaged object should be at least at 20° above the horizon to prevent atmospheric extinction. Apart from atmospheric conditions and light pollution, these conditions can be calculated using the observer location, date and time, and of course, the object itself.

This utility shows whether the sky is dark or not for each given date and location. It displays one of three possible conditions, every 30 minutes: dark sky, Moon above horizon or dusk/dawn/day.

## Getting Started

### Prerequisites

This script needs Python 3 and [PyEphem](https://rhodesmill.org/pyephem/) library.

- Fedora: python3-pyephem
- Ubuntu: python3-ephem
- SuSE: python3-ephem

### Execution

Using the command line:

```
./python3 qitime.py --lat <latitude> --lon <longitude> --date <yyyy-mm-dd>

Quality Imaging Time
= Observer
  Date:2020/2/20 00:00:00       Lon:-15:25:00.0 Lat:28:00:00.0
= Rise/Transit/Set
  Sun   Rise:2020-02-20 07:33:24.000003 Transit:2020-02-20 13:15:25.000003      Set:2020-02-20 18:57:48.000003
  Moon  Rise:2020-02-20 05:32:03.000003 Transit:2020-02-20 10:53:10.000003      Set:2020-02-20 16:15:41.000003
= Twilight
  Quality       Dawn:2020-02-20 20:00:38.000003 Dusk:2020-02-20 06:30:36.000003
= Dark night (without any Moon)
  Darkness (Quality)    Start:2020-02-20 20:00:38.000003        End:2020-02-20 06:30:36.000003
  00  01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  16  17  18  19  20  21  22  23   Moon phase
  🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌘🌘🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌌🌌🌌🌌🌌🌌🌌 🌘
```

## Virtual environment

A poetry file is provided to install needed packages into a virtual environment

You can install poetry using pip executing the following command

    pip install poetry --user

For more information about poetry you can read the [Poetry documentation site](https://python-poetry.org/docs/)

After installing poetry just run:

    poetry install

This will install the virtual environment and needed modules.

Now to run the script, execute the following command

    poetry run python qitime.py --lat <latitude> --lon <longitude> --date <yyyy-mm-dd>


## Development

For developers a [pre-commit](https://pre-commit.com/) configuration is provided so the code is checked and linted properly before committing.

You can install pre-commit using pip executing the following command

    pip install pre-commit --user

Then, to install the git pre-commit hook

    pre-commit install

After that, on each commit the code will be checked previously. To run a check without committing you can execute the following command:

    pre-commit run  --all-files

The pre-commit configuration will automatically format the code using [black](https://black.readthedocs.io/en/stable/) and run several checks.

## Authors

* Víctor R. Ruiz

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
