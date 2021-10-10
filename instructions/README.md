# Asteroid Hunter :: v1.1.0

NASA has asked us to help create a data pipeline for NeoWs (Near Earth Object Web Service), which is a system that tracks asteroids and their approaches to Earth. They have asked us to create functions that extract specific data sets for their research.

## NASA APIs

Browse the NASA APIs and generate an API Key:

- [NASA APIs](https://api.nasa.gov/)

In the accordian menu at the bottom of the page look for the following API:

- `Asteroids - NeoWs`

## Environment Requirements

The technical requirements listed below are the baseline for the project, but please feel free to use any standard Python packages (`json`, `os`, `pprint`, `datetime`, etc).

### Installing Python

Install the `pyenv` formulae for Homebrew to manage Python versions:

- [Pyenv](https://formulae.brew.sh/formula/pyenv)

```unix
brew install pyenv
```

After installing `pyenv` run:

```unix
pyenv install 3.8.7
```

When the installation process is complete run:

```unix
pyenv global 3.8.7
```

Close and reopen your terminal.

### Virtual Environments and Dependency Management

Use `Python Poetry` for virtual environment and dependency management:

- [Python Poetry](https://python-poetry.org/)

```unix
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Poetry is what we use at Mashey to manage the virtual environments and dependencies of our projects. If you are new to Python virtual environments please read this article:

[Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)

### Python Packages

Python packages that make designing modular software easier are generally available on [PyPi](https://pypi.org/), which is the most popular Python package hosting platform.

[Optional]

If you are new to Python the following links are great for building understanding, but are not required for this code challenge.

- For more information about packages and modules check out this great [RealPython article](https://realpython.com/python-modules-packages/).
- For more information about how to import Python packages and modules check out this [RealPython article](https://realpython.com/python-import/).

#### Requests

For handling HTTP use the `requests` package

- [Requests](https://pypi.org/project/requests/)

The `requests` package is how you should interact with the Asteroids API. Documentation can be found [here](https://requests.readthedocs.io/en/master/).

#### Pytest

Test your code with `pytest`:

- [Pytest](https://pypi.org/project/pytest/)

PyTest is our preferred testing package. Documentation can be found [here](https://docs.pytest.org/en/stable/index.html).

#### VCRPY (optional)

If you would like to record the Asteroid API responses on cassettes in order to help avoid hitting the API rate limit please use:

- [VCRPY](https://pypi.org/project/vcrpy/)
  - [Documentaton](https://vcrpy.readthedocs.io/en/latest/)

This is not required, but if you have experience with recording cassettes of API responses it could be helpful.

## Project Requirements

The most important aspect of this challenge is to write clean and modular code with developer empathy in mind. An incomplete submission that contains solid logic, good organization, and well-tested code would be preferred to a complete submission that is logically inconsistent, disorganized, and not well-tested.

The code review of your submission will focus on solid fundamentals and a growth mindset.

Here is a gift from Mashey for being a potential new member of our team:

- [Python 3 Cheat Sheet](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-hello-world/cheatsheet)

Please create the following functions.

### `asteroid_closest_approach()`

Endpoint: `https://api.nasa.gov/neo/rest/v1/neo/browse`

This function should return `JSON` data that includes each asteroid and its closest approach to Earth. There are 1246 pages of data, so please design your function to traverse all pages. It's possible that you'll hit the API request limit, but that's okay provided your code successfully traverses the response pages up to that point.

The `close_approach_data` field is a list of all approaches for a given asteroid, but only the closest approach should be returned. Here is an example of the expected `JSON` data structure that should be returned for each asteroid:

```json
{
    "links": {
        "self": "http://www.neowsapp.com/rest/v1/neo/2000433?api_key=DEMO_KEY"
    },
    "id": "2000433",
    "neo_reference_id": "2000433",
    "name": "433 Eros (A898 PA)",
    "name_limited": "Eros",
    "designation": "433",
    "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2000433",
    "absolute_magnitude_h": 10.4,
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 22.1082810359,
            "estimated_diameter_max": 49.435619262
        },
        "meters": {
            "estimated_diameter_min": 22108.281035909,
            "estimated_diameter_max": 49435.619261962
        },
        "miles": {
            "estimated_diameter_min": 13.7374446956,
            "estimated_diameter_max": 30.7178601764
        },
        "feet": {
            "estimated_diameter_min": 72533.7327538517,
            "estimated_diameter_max": 162190.3570994153
        }
    },
    "is_potentially_hazardous_asteroid": false,
    "close_approach_data": [
        {
            "close_approach_date": "1900-12-27",
            "close_approach_date_full": "1900-Dec-27 01:30",
            "epoch_date_close_approach": -2177879400000,
            "relative_velocity": {
                "kilometers_per_second": "5.5786203614",
                "kilometers_per_hour": "20083.0333009607",
                "miles_per_hour": "12478.8158863664"
            },
            "miss_distance": {
                "astronomical": "0.3149291092",
                "lunar": "122.5074234788",
                "kilometers": "47112723.937317404",
                "miles": "29274489.1785480152"
            },
            "orbiting_body": "Earth"
        }
    ],
    "orbital_data": {
        "orbit_id": "658",
        "orbit_determination_date": "2020-09-06 18:22:27",
        "first_observation_date": "1893-10-29",
        "last_observation_date": "2020-09-03",
        "data_arc_in_days": 46330,
        "observations_used": 8767,
        "orbit_uncertainty": "0",
        "minimum_orbit_intersection": ".148623",
        "jupiter_tisserand_invariant": "4.582",
        "epoch_osculation": "2459000.5",
        "eccentricity": ".2229512647434284",
        "semi_major_axis": "1.458045729081037",
        "inclination": "10.83054121829922",
        "ascending_node_longitude": "304.2993259000444",
        "orbital_period": "643.0654021001488",
        "perihelion_distance": "1.132972589728666",
        "perihelion_argument": "178.8822959227224",
        "aphelion_distance": "1.783118868433408",
        "perihelion_time": "2459159.351922368362",
        "mean_anomaly": "271.0717325705167",
        "mean_motion": ".5598186418120109",
        "equinox": "J2000",
        "orbit_class": {
            "orbit_class_type": "AMO",
            "orbit_class_description": "Near-Earth asteroid orbits similar to that of 1221 Amor",
            "orbit_class_range": "1.017 AU < q (perihelion) < 1.3 AU"
        },
        "is_sentry_object": false
    }
}
```

### `month_closest_approaches()`

Endpoint: `https://api.nasa.gov/neo/rest/v1/feed?start_date=2021-01-01&end_date=2021-01-08`

Date Format: `YEAR-MONTH-DAY`

This function should return `JSON` data that includes all the closest asteroid approaches in a given calendar month, including a total `element_count` for the month. Please keep in mind that the endpoint is only able to return 7 days of data at a time.

### `nearest_misses()`

Endpoint: `https://api.nasa.gov/neo/rest/v1/neo/browse`

This function should return `JSON` data that includes the 10 nearest misses, historical or expected, of asteroids impacting Earth. For each nearest miss please return the asteroid data, including the nearest miss in `close_approach_data`, but excluding any additional `close_approach_data`. Here is an example of the expected `JSON` data structure that should be returned for each nearest miss:

```json
{
    "links": {
        "self": "http://www.neowsapp.com/rest/v1/neo/2000433?api_key=DEMO_KEY"
    },
    "id": "2000433",
    "neo_reference_id": "2000433",
    "name": "433 Eros (A898 PA)",
    "name_limited": "Eros",
    "designation": "433",
    "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2000433",
    "absolute_magnitude_h": 10.4,
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 22.1082810359,
            "estimated_diameter_max": 49.435619262
        },
        "meters": {
            "estimated_diameter_min": 22108.281035909,
            "estimated_diameter_max": 49435.619261962
        },
        "miles": {
            "estimated_diameter_min": 13.7374446956,
            "estimated_diameter_max": 30.7178601764
        },
        "feet": {
            "estimated_diameter_min": 72533.7327538517,
            "estimated_diameter_max": 162190.3570994153
        }
    },
    "is_potentially_hazardous_asteroid": false,
    "close_approach_data": [
        {
            "close_approach_date": "1900-12-27",
            "close_approach_date_full": "1900-Dec-27 01:30",
            "epoch_date_close_approach": -2177879400000,
            "relative_velocity": {
                "kilometers_per_second": "5.5786203614",
                "kilometers_per_hour": "20083.0333009607",
                "miles_per_hour": "12478.8158863664"
            },
            "miss_distance": {
                "astronomical": "0.3149291092",
                "lunar": "122.5074234788",
                "kilometers": "47112723.937317404",
                "miles": "29274489.1785480152"
            },
            "orbiting_body": "Earth"
        }
    ],
    "orbital_data": {
        "orbit_id": "658",
        "orbit_determination_date": "2020-09-06 18:22:27",
        "first_observation_date": "1893-10-29",
        "last_observation_date": "2020-09-03",
        "data_arc_in_days": 46330,
        "observations_used": 8767,
        "orbit_uncertainty": "0",
        "minimum_orbit_intersection": ".148623",
        "jupiter_tisserand_invariant": "4.582",
        "epoch_osculation": "2459000.5",
        "eccentricity": ".2229512647434284",
        "semi_major_axis": "1.458045729081037",
        "inclination": "10.83054121829922",
        "ascending_node_longitude": "304.2993259000444",
        "orbital_period": "643.0654021001488",
        "perihelion_distance": "1.132972589728666",
        "perihelion_argument": "178.8822959227224",
        "aphelion_distance": "1.783118868433408",
        "perihelion_time": "2459159.351922368362",
        "mean_anomaly": "271.0717325705167",
        "mean_motion": ".5598186418120109",
        "equinox": "J2000",
        "orbit_class": {
            "orbit_class_type": "AMO",
            "orbit_class_description": "Near-Earth asteroid orbits similar to that of 1221 Amor",
            "orbit_class_range": "1.017 AU < q (perihelion) < 1.3 AU"
        },
        "is_sentry_object": false
    }
}
```
