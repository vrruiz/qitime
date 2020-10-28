#!/usr/bin/python3
"""
qitime - Quality Imaging Time
(C) 2020 Victor R. Ruiz <rvr@linotipo.es>

Calculates the Quality Imaging Time (dark hours) for a given date.
Based on a concept developed by Charles Bracken:
https://digitalstars.wordpress.com/
"""

import argparse
import datetime

import ephem


def get_lunar_phase(lunation):
    if lunation < 6.25 or lunation > 93.75:
        phase = "🌑"
    elif lunation < 18.75:
        phase = "🌒"
    elif lunation < 31.25:
        phase = "🌓"
    elif lunation < 43.75:
        phase = "🌔"
    elif lunation < 56.25:
        phase = "🌕"
    elif lunation < 68.75:
        phase = "🌖"
    elif lunation < 81.25:
        phase = "🌗"
    elif lunation <= 93.75:
        phase = "🌘"
    return phase


def get_total_dark_hours(dusk, dawn):
    midnight_prev = datetime.datetime(dusk.year, dusk.month, dusk.day, 23, 59, 59)
    midnight_next = datetime.datetime(dawn.year, dawn.month, dawn.day)
    prev_hours = midnight_prev - dusk
    next_hours = dawn - midnight_next
    return prev_hours + next_hours


def quality_time(
    date_time,
    latitude,
    longitude,
    moon_display=False,
    debug=False,
):
    """ Calculate quality time. """
    # Observer data
    observer = ephem.Observer()
    observer.lon = latitude
    observer.lat = longitude
    observer.elevation = 0
    observer.pressure = 1013  # USNO
    observer.temp = 10
    observer.horizon = "-0:34"  # USNO
    observer.date = date_time  # Local time

    if debug:
        print("= Observer")
        print(
            "  Date:{}\tLon:{}\tLat:{}".format(
                observer.date, observer.lon, observer.lat
            )
        )

    # Objects
    sun = ephem.Sun()
    moon = ephem.Moon()
    # Compute
    sun.compute(observer)
    moon.compute(observer)
    # Calculate moon phase
    next_new_moon = ephem.next_new_moon(observer.date)
    prev_new_moon = ephem.previous_new_moon(observer.date)
    # 50 = full moon, 0 = new moon
    lunation = (
        float(observer.date - prev_new_moon) / (next_new_moon - prev_new_moon) * 100
    )

    objects = {"Sun": sun, "Moon": moon}
    times = {}

    if debug:
        print("= Rise/Transit/Set")
    for target in objects:
        t = objects[target]
        times[target] = {
            "rise": None,
            "transit": None,
            "set": None,
            "always_up": False,
            "never_up": False,
        }
        try:
            times[target]["rise"] = ephem.localtime(
                observer.next_rising(t, use_center=True)
            )
            times[target]["transit"] = ephem.localtime(observer.next_transit(t))
            times[target]["set"] = ephem.localtime(
                observer.next_setting(t, use_center=True)
            )
            if debug:
                print(
                    "  {}\tRise:{}\tTransit:{}\tSet:{}".format(
                        target,
                        times[target]["rise"],
                        times[target]["transit"],
                        times[target]["set"],
                    )
                )
        except ephem.AlwaysUpError:
            if debug:
                print(f"  {target} always up")
            times[target]["always_up"] = True
        except ephem.NeverUpError:
            if debug:
                print(f"  {target} never up")
            times[target]["never_up"] = True

    # Twilight
    # https://stackoverflow.com/questions/2637293/calculating-dawn-and-sunset-times-using-pyephem
    # fred.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
    if debug:
        print("= Twilight")
    twilight = {
        # 'Civil': '-6',
        # 'Nautical': '-12',
        "Quality": "-15",
        # 'Astronomical': '-18'
    }
    for twilight_type in twilight:
        observer.horizon = twilight[twilight_type]
        dawn_t = f"{twilight_type}_dawn"
        dusk_t = f"{twilight_type}_dusk"
        always_t = f"{twilight_type}_always"
        never_t = f"{twilight_type}_never"
        times[dawn_t] = None
        times[dusk_t] = None
        times[always_t] = False
        times[never_t] = False
        try:
            # Calculate twilight times
            times[dusk_t] = ephem.localtime(observer.next_setting(sun, use_center=True))
            times[dawn_t] = ephem.localtime(observer.next_rising(sun, use_center=True))
            if debug:
                print(
                    "  {}\tDawn:{}\tDusk:{}".format(
                        twilight_type, times[dusk_t], times[dawn_t]
                    )
                )
        except ephem.AlwaysUpError:
            times[always_t] = True
            if debug:
                print(f"  There is not {twilight_type} night")
        except ephem.NeverUpError:
            times[never_t] = True
            if debug:
                print(f"  There is not {twilight_type} night")

    # Dark Night
    if debug:
        print("= Dark night (without any Moon)")
    # Calculate limits
    for twilight_type in twilight:
        dawn_t = f"{twilight_type}_dawn"
        dusk_t = f"{twilight_type}_dusk"
        always_t = f"{twilight_type}_always"
        never_t = f"{twilight_type}_never"
        if debug:
            print(
                "  Darkness ({})\tStart:{}\tEnd:{}".format(
                    twilight_type, times[dusk_t], times[dawn_t]
                )
            )
            total_dark_hours = get_total_dark_hours(times[dusk_t], times[dawn_t])
            print(f"  Total dark hours: {total_dark_hours}")
        dt = observer.date.datetime()
        if debug:
            print("  ", end="")
            for i in range(0, 24):
                print(f"{i:02}  ", end="")
            print(" Moon phase")
        print("  ", end="")

        # Get lunar phase
        phase = get_lunar_phase(lunation)

        for h in range(0, 24):
            for m in [0, 30]:
                current_date = ephem.localtime(
                    ephem.Date(
                        "{}-{}-{} {:02d}:{:02d}:00".format(
                            dt.year, dt.month, dt.day, h, m
                        )
                    )
                )
                if times[always_t]:
                    print("🌞", end="")
                elif (
                    not times[never_t] and times[dawn_t] < current_date < times[dusk_t]
                ):
                    print("🌞", end="")
                elif moon_display:
                    observer.horizon = "0"
                    observer.date = current_date
                    moon.compute(observer)
                    if moon.alt > 0:
                        print(phase, end="")
                    else:
                        print("🌌", end="")
                else:
                    print("🌌", end="")
        print(f" {phase}")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", help="Observer latitude", required=True)
    parser.add_argument("--lon", help="Observer longitude", required=True)
    parser.add_argument("--date", help="Date to calculate ephemeris", required=True)
    args = parser.parse_args()

    # Display header
    print("Quality Imaging Time")
    # Calculate and display Quality Imaging ephemeris
    quality_time(
        args.date,
        latitude=args.lat,
        longitude=args.lon,
        debug=True,
        moon_display=True,
    )
