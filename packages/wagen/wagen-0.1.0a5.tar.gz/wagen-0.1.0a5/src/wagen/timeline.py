"""Create timeline for multi-day hike/adventure that uses estimated pace to
predict time to reach each waypoint. Use given day start time or a
start derived from sunrise local to hike. Warn if estimate arrival at camp
or car is too close to sunset.

Create a set of Deviation Tables that can be used (without
electronics) to determine the approximate affect changes in pace will
be on day finish time.

IMPLEMENTATON:
Try to uses fewer python loops in favor of dataframe arithmetic.  It
will be more spreadsheet like that way and probably more flexible.
"""

import csv
from pathlib import Path
import datetime as dt
from pprint import pp
from zoneinfo import ZoneInfo # to get tzinfo from timezone name
from collections import defaultdict
from warnings import warn

import pandas as pd
import numpy as np
from IPython.display import Markdown, HTML

from wagen import sun
import wagen.caltopo_io as cti


EXAMPLE_seg_pace = { # in minutes per mile
    'DEFAULT': 60, #20,
    'New Hance': 30,
    'Tonto 2': 20,
    'up GV': 30,
}


# caltopo_df min columns: day, segment, distance
def apply_seg_paces(df, seg_pace):
    default_pace = seg_pace.get('DEFAULT', 60)
    p_df = df.reset_index().assign(
        pace=df['segment'].map(lambda r: seg_pace.get(r, default_pace)),
        minutes=lambda r: r['distance'] * r['pace'],
        ).drop(columns=['waypoint'])
    #!print(f'apply_seg_paces 1: {p_df.columns.to_list()=} {len(p_df)=}')

    #!sum_cols = ['aeg', 'ael', 'distance', 'break_time', 'minutes']
    agg_cols = {
        'day':'last',
        'segment':'last',
        'distance':'sum',
        'aeg':'sum',
        'ael':'sum',
        'break_time':'sum',
        'pace':'last',
        'minutes':'sum',
        #!'cs_dist':'last',
        #!'cs_mins':'last',
        #!'day_dist':'last',
        #!'rem_dist':'last',
        #!'day_mins':'last',
        #!'rem_mins':'last',
        #!'waypoint':'last',
    }

    day_df = p_df.groupby('day').agg(agg_cols)
    #!seg_total = p_df.groupby('segment', sort=False).agg(agg_cols)
    seg_df = p_df.groupby('segment', sort=False).agg(agg_cols)
    #!print(f'apply_seg_paces 2: {seg_df.columns.to_list()=} {len(seg_df)=}')

    predicted_df = seg_df.assign(
        cs_dist=seg_df.groupby('day')[['distance']].cumsum(),
        cs_mins=seg_df.groupby('day')[['minutes']].cumsum(),
        day_dist=seg_df['day'].map(lambda d: day_df.loc[d ,'distance']),
        rem_dist=lambda r: r['day_dist'] - r['cs_dist'],
        day_mins=seg_df['day'].map(lambda d: day_df.loc[d ,'minutes']),
        rem_mins=lambda r: r['day_mins'] - r['cs_mins'],
    )
    return predicted_df
    #!
    #! #return predicted_df, seg_total, day_df
    #! print(f'apply_seg_paces 3: {predicted_df.columns.to_list()=} {len(predicted_df)=}')
    #! #!return predicted_df.groupby('segment', sort=False).agg('last')
    #! seg_df = predicted_df.groupby('segment', sort=False).agg('last')
    #! print(f'apply_seg_paces 4: {seg_df.columns.to_list()=}')
    #! return seg_df

def predict_clock_time(predicted_df):
    df = predicted_df
    move_df = df.assign(td=df['minutes'].map(
        lambda r: pd.Timedelta(minutes=r)))
    return move_df

# Round to 1/4 (hour)
def round_hr(h):
    return round(h * 4, 0)/4

# Predict the difference between Actual and (originally) Predicted
# minutes of hiking for a day given a partially hiked day.
class UpdateArrival():
    def __init__(self, seg_df, default_pace=60, seg_paces={}):
        """
        seg_paces:: dict() => lut[seg_name] => minutes_per_mile
        """
        reqd_cols = {'day',  'segment',
                     'distance', 'cs_dist', 'day_dist', 'rem_dist',
                     'break_time', 'pace', 'minutes',
                     'rem_mins', 'cs_mins',  'day_mins',
                     }
        missing = reqd_cols - set(seg_df.columns)
        assert reqd_cols <= set(seg_df.columns), f'seg_df columns {missing=}'
        self.seg_df = seg_df
        self.default_pace = default_pace

    def here_dist(self, seg_name):
        return self.seg_df.loc[seg_name,'cs_dist']

    def __repr__(self):
        return (f'segment_names={self.seg_df.index.to_list()}'
                )

    def dbg(self, method):
        print(f'{method}: '
              f'Minutes to camp changed from '
              f'{pred_day_mins=:.0f} to {new_day_mins=:.0f} '
              f'({pred_day_mins/60:.1f} to {new_day_mins/60:.1f}) ')

    def pred_day_mins(self, seg_name):
        return round(self.seg_df.loc[seg_name, 'day_mins'])

    def pred_here_mins(self, seg_name):
        return round(self.seg_df.loc[seg_name, 'cs_mins'])

    def pred_post(self, seg_name):
        return self.pred_day_mins(seg_name) - self.pred_here_mins(seg_name)

    # Return new_day_hours rounded to 1/4 hour.
    def multiply_future(self, seg_name, here_mins, factor=1):
        new_day_mins = here_mins + self.pred_post(seg_name) * factor
        return round_hr(new_day_mins/60)

    # Use the same percent deviation of actual/predicted pace for
    # remainder of hike as we actually observed up to this point.
    # Multiply that pace by FUDGE.
    # Return new_day_hours rounded to 1/4 hour.
    def future_as_previous(self, seg_name, here_mins, fudge=1, verbose=False):
        factor = here_mins / self.pred_here_mins(seg_name)  # Actual/Predicted
        new_day_mins = here_mins + self.pred_post(seg_name) * factor * fudge
        if verbose:
            print(f'{here_mins=} {factor=} {new_day_mins=}')
        #!return int(new_day_mins)
        return round_hr(new_day_mins/60)

    def future_deviations(self, seg_name, here_mins):
        here_factor = here_mins / self.pred_here_mins(seg_name)
        new = [self.multiply_future(seg_name, here_mins, fudge=f)/60
               for f in [here_factor, 1, 1/here_factor]]
        return new, float(here_factor)

    # Use actual pace to HERE as value in calculating pace for day REMAINDER.
    def arrive_table_ratio(self, seg_name,
                           min_hrs=2, max_hrs=6, step=0.5,  **kwargs):
        # might want to adjust these based on experience using WAGEN
        fudges = [0.50, 0.75, 0.90, 1.00, 1.10, 1.25, 1.50]

        # here_hours < predicted are not really important to us
        here_hours_list = np.arange(min_hrs, max_hrs + 1e-5, step)

        records = list()
        for hr in here_hours_list:
            here_hours = hr
            here_mins = hr * 60
            pred_day_hours = {
                f'{f:.0%}': self.future_as_previous(seg_name, here_mins, fudge=f)
                for f in fudges}
            here_deviation = here_mins - self.pred_here_mins(seg_name)
            rec = dict(
                here_hours=here_hours,
                _hd=here_deviation/60,
                **pred_day_hours
                )
            records.append(rec)
        return pd.DataFrame(records)

    # Use orginal paces for REMAINDER of day in calculating new REMAINDER paces.
    def arrive_table_pace(self, seg_name,
                          min_hrs=2, max_hrs=6, step=0.5,  **kwargs):
        # might want to adjust these based on experience using WAGEN
        factors = [0.50, 0.75, 0.90, 1.00, 1.10, 1.25, 1.50]

        # here_hours < predicted are not really important to us
        here_hours_list = np.arange(min_hrs, max_hrs + 1e-5, step)

        records = list()
        for hr in here_hours_list:
            here_hours = hr
            here_mins = hr * 60
            pred_day_hours = {
                f'{f:.0%}': self.multiply_future(seg_name, here_mins, f)/60
                for f in factors}
            here_deviation = here_mins - self.pred_here_mins(seg_name)
            rec = dict(
                here_hours=here_hours,
                _hd=here_deviation/60,
                **pred_day_hours
                )
            records.append(rec)
        return pd.DataFrame(records)


    def arrive_table(self, seg_name, adjust='ratio', **kwargs):
        """ Produce static lookup table.
        Lookup nearest Hours at completion of Seg in row header.
        Lookup expected % deviation of remaining hike in col header.
        Read new time expected to arrive at camp or car from cell.

        adjust: Changes the method used to predict the pace uses to calculate
           segments for the remainder of the day.
        """
        match adjust:
            case 'ratio':
                return self.arrive_table_ratio(seg_name, **kwargs)
            case 'pace':  # multiple remaining paces by factor
                return self.arrive_table_pace(seg_name, **kwargs)
            case _:
                warn(f'No method for: {adjust=}. Using adjust="ratio"',
                     stacklevel=2)
                return self.arrive_table_ratio(seg_name, **kwargs)


# seg_paces = { 'DEFAULT': 60, 'New Hance': 30, 'Tonto 2': 20, 'up GV': 30}
def seg_pace_df(caltopo_csvfname, seg_pace):
    sum_cols = ['aeg', 'ael', 'distance', 'break_time']
    EXAMPLE_seg_pace = { # in minutes per mile
        'DEFAULT': 60, #20,
        'New Hance': 30,
        #'Tonto': 60,
        'Tonto 2': 20,
        #'Up W arm': 60,
        #'West arm option OB': 60,
        #'GV tr': 60,
        'up GV': 30,
    }

    df, trip = cti.travelplan_multi_csv(csvfname=caltopo_csvfname)
    #!pred_df, seg_df, day_df = apply_seg_paces(df, seg_pace)
    seg_df = apply_seg_paces(df, seg_pace)

    #cols=['day', 'distance', 'pace', 'minutes', 'cs_dist', 'cs_mins',
    #      'day_dist', 'rem_dist', 'day_mins', 'rem_mins']
    #!return pred_df, seg_df, day_df
    return seg_df

# Make the artifact tables good for use ON TRAIL in PRINTED format.
def make_table_pretty(styler, daylight=8):
    #! styler.set_caption("Day Travel time")
    styler.format(precision=2)
    styler.format_index(precision=1)
    styler.apply(lambda x:
                 ['background: lightblue' if x.name == '100%'  else '' for i in x])
    styler.map(lambda x: 'background-color: yellow' if x > daylight else '')
    return styler

# Remove _hd.
# Convert "hrs" column into index (or remove useless index for more concise)
# Highlight "100%" column.
# Gray cells (predicted hrs to camp) that exceed number of daylight hours.
#
# Generate a table for every segment except that last one of a day.
# (Nothing to predict there since we are at camp/car at end of day)
def gen_artifacts(caltopo_csvfname,
                  seg_paces=None,
                  default_pace=60,
                  adjust='pace', daylight=12, verbose=False):
    if seg_paces is None:
        warn(f'No paces given for segments (seg_paces). '
             f'Using paces from CSV file '
             f'(or {default_pace=} minutes/mile if not available).',
             stacklevel=2)
        seg_paces = { 'DEFAULT': default_pace}
    seg_df = seg_pace_df(caltopo_csvfname, seg_paces)
    seg_list = seg_df['segment'].to_list()
    segds_df = seg_df.set_index(['day', 'segment'])
    seg_lut = {name:day for (day,name) in segds_df.index}

    if verbose:
        print(f'gen_artifacts: {seg_df.columns.to_list()=}')

    day_df = seg_df.groupby('day').agg('last')

    print(f'\nTrip Segments: {seg_list}\n')
    for day in day_df.index:
        last_seg = day_df.loc[day,'segment']
        day_hrs = round_hr(day_df.loc[day,'day_mins']/60)
        day_dist = round(day_df.loc[day,'cs_dist'],1)
        #!print(f'{last_seg=}')

        for seg_name in seg_df.index:
            if day != seg_lut[seg_name]:
                continue

            # Display info about end of segment
            seg_dist = round(seg_df.loc[seg_name,'distance'], 1)
            seg_pace = round(seg_df.loc[seg_name,'pace'], 0)
            seg_hrs  = round_hr(seg_df.loc[seg_name,'minutes']/60)
            here_hrs = round_hr(seg_df.loc[seg_name,'cs_mins']/60)
            here_dist = round(seg_df.loc[seg_name,'cs_dist'], 1)
            display(HTML('<hr/>'))
            print(f'Day={day} Segment={seg_name!r} Distance={seg_dist}\n'
                  f'PREDICTED SEGMENT: Pace={seg_pace} Hours={seg_hrs}\n'
                  f'PREDICTED PROGRESS: Start to Here/Day (%) \n'
                  f'  Distance: '
                  f'{here_dist:>5.1f} / {day_dist:>5.1f} ({here_dist/day_dist:.0%}); '
                  f'(miles) \n'

                  f'  Time:     '
                  f'{here_hrs:>5.2f} / {day_hrs:>5.2f} ({here_hrs/day_hrs:.0%}); '
                  f'(hours) Originaly Predicted'
                  )

            if seg_name == last_seg:
                print('No table output for LAST SEGEMENT of the day. '
                      'You are done so there is nothing to predict!\n'
                      )
            if seg_name == last_seg:
                # ignore last segment of each day since we finish at camp/car!
                continue

            tab = UpdateArrival(seg_df).arrive_table(seg_name, adjust=adjust).round(2)
            # .round(2)
            pptab = tab.drop(columns='_hd').rename(columns={'here_hours':'hrs'}).set_index('hrs')
            styled_df = pptab.style.pipe(make_table_pretty, daylight=daylight)
            display(styled_df)
    return (styled_df, seg_df)

##############################################################################

# given start time for each day, calc end time and hours from sunset!!!
# Get elevation (meters) from lat,lon
# https://api.open-elevation.com/api/v1/lookup?locations=41.161758,-8.583933
def timeline(trip_df, trip,
             start_time: dt.datetime | None = None, # sunrise today
             tzid: str = 'America/Phoenix',
             morning_daylight: float=1.5, # reqd hours @ camp after twilight
             evening_daylight: float=2.0, # reqd hours @ camp before sunset
             include_dt = False,
             rename = False,
             ):
    """Assume hiking will start the same time every day.
    Consider adding "BEGIN" waypoint for day specific start time!!!

    Returned DataFrame:
    Each row is a "leg".  Multiple legs delimited in Segment by Waypoints.
    COLUMNS:
      date: ISO String (YYYY-MM-DD)
      time: ISO String (HH:MM)
      day: (int) day number of travel
      seg: (str) Segment name (starting)
      waypoint: waypoint along leg (from CalTop "marker")
      distance: (miles) of leg
      aeg: (feet) Accumulated Elevation Gain over leg
      ael: (feet) Accumulated Elevation Loss over leg
      duration: (minutes) PREDICTED travel time for leg
      break_time: (minutes) PREDICTED non-travel time for leg
      spent_time: (hours) Accumated time for predicted travel + breaks
      elevation: (feet) Hight above sea-level at waypoint
      hours: (hours) PREDICTED duration + break_time
      pace: (minutes/mile) PREDICT rate of travel
    REMOVED columns:
      alert: (str) Message when Estimate day finish is too close to sunset.

    """

    #!print(f'timeline: {trip=} {start_time=} {tzid=} {morning_daylight=} {evening_daylight=} {include_dt=}')

    trip_meta = trip.copy()
    df = trip_df.copy(deep=True)
    day_minutes = 0
    prev_done_time = None
    eod = False
    eod_times = dict()

    lat, lon = trip['start_latlon']
    sunset, twilight, sunrise = sun.sun_set_rise(
        lat,
        lon,
        date=str(start_time)[:10].replace('-',''),
        tzid=tzid,
        formatted=0)

    # Modify start_time if does not contain both date and meaningful time.
    if start_time is None:
        start_time = dt.datetime.today()

    if start_time.hour == 0 and start_time.minute == 0:
        start_time = start_time.replace(hour=twilight.hour,
                                        minute=twilight.minute,
                                        tzinfo=twilight.tzinfo,
                                        second=0, microsecond=0)
        start_time += dt.timedelta(hours=morning_daylight)


    first_date = start_time.date()
    day_start_time = start_time.time()
    trip_meta = dict(
        first_date=first_date.isoformat(),
        day_start_time=day_start_time.strftime("%H:%M"),
        twilight=twilight.isoformat(),
        sunrise=sunrise.isoformat(),
        sunset=sunset.isoformat(),
        start_latlon=trip['start_latlon'],
        start_elevation=trip['start_elevation'],
        morning_daylight=morning_daylight,
        evening_daylight=evening_daylight,
        tzid=tzid,
        )

    for index, row in trip_df.iterrows():
        # Only do this on the first segment Start of the day
        if row['waypoint'] == 'Start' and eod:
            day_minutes = 0
            eod = False
        day_minutes += row.duration + row.break_time
        #!df.at[index, 'day_minutes'] = day_minutes
        row_dt = (dt.datetime.combine(first_date,
                                      day_start_time,
                                      sunrise.tzinfo)
                  + dt.timedelta(days=row['day']-1, minutes=day_minutes))
        #!!! df.at[index, 'deviation'] = row_dt.date()
        # see: https://docs.google.com/spreadsheets/d/1-DNLDEDKi286bAzVmbptdajS_mAE8OeM1oqFAemgrF4/edit?usp=sharing

        #!if (row_dt.time() > (sunset
        #!                     - dt.timedelta(hours=evening_daylight)).time()):
        #!    df.at[index, 'alert'] = "LATE to CAMP"
        #!else:
        #!    df.at[index, 'alert'] = ''


        df.at[index, 'date'] = row_dt.date()
        done_time = row_dt.time()
        #!ldt = '' if prev_done_time == done_time else done_time.strftime("%H:%M")
        ldt = done_time.strftime("%H:%M")
        prev_done_time = done_time
        df.at[index, 'time'] = ldt
        df.at[index, 'spent_time'] = day_minutes/60.0
        df.at[index, 'dt'] = row_dt

        #!if row['waypoint'] in ['camp','car']: # 'EOD':
        if row['waypoint'] in ['camp','car']:
            eod = True
            eod_times[row['day']] = done_time
    # END for trip_df.iterrows

    final_column_order = ['date','time','day', 'waypoint',
                          'distance', 'aeg','ael','spent_time',
                          'duration', 'break_time',
                          'elevation', 'hours', 'pace',
                          'segment',
                          # 'alert',
                          # 'trip_leg','elapsed',
                          ]
    if include_dt:
        final_column_order.append('dt')

    df = df[final_column_order]

    #df.drop(['segment','dt', 'day'], axis="columns", inplace=True)
    if rename:
        renames = {c: c.title() for c in df.columns}
        renames.update({
            'distance': 'Distance (miles)',
            'aeg': 'AEG (ft)',
            'ael': 'AEL (ft)',
            'spent_time': 'Day Spent Time (hrs)',
            'duration': 'Leg Travel Time (mins)',
            'break_time': 'Leg Break (mins)',
            'pace': 'Pace (mins/mi)',
            })
        df.rename(columns=renames, inplace=True)
        df.set_index(['Date', 'Time'], inplace=True)
    trip_meta['eod_times'] = eod_times
    return df, trip_meta

def trip_timeline(csvfname, **kwargs):
    caltopo_df, trip = cti.travelplan_multi_csv(csvfname, caltopo_predictions=True)
    timeline_df, meta = timeline(caltopo_df, trip, **kwargs)
    #!return timeline_df, trip, meta
    return timeline_df, meta


# Aware, Predict, Embrace
# predictions:: dict(segment) = pace_mm
# In Colummns: segment, day, waypoint, distance
# RESULTS: deviation tables
def ape_timeline(caltopo_df, predictions, start_time,
                 first_date = dt.date.today(),
                 tzid: str = 'America/Phoenix',):
    out_columns = ['day', 'segment', 'waypoint', 'distance',
                   'break_time', 'move_time',
                   'date', 'time',
                   'pace',
                   #'dt'
                   ]
    use_caltopo_cols = ['day', 'segment', 'waypoint', 'distance', 'break_time']
    df = caltopo_df[use_caltopo_cols].copy(deep=True)
    sod = True # Start Of Day

    #!day_segments = defaultdict(set) # dict(day) => {seg_name1, seg_name2, ...}

    default_pace = predictions.get('DEFAULT',60) # minutes/mile
    eod_times = dict() # eod_times[day] => TimeofdayTravelEnds
    #!seg_duration = defaultdict(int) # dict(seg_name) => minutes

    for index, row in df.iterrows():
        day = row['day']
        seg_name = row['segment']

        #!day_segments[day].add(seg_name)

        # Accumulate minutes of PREDICTED segment time (travel + rest)
        pace = predictions.get(seg_name, default_pace)
        df.at[index, 'move_time'] = row['distance'] * pace
        #!seg_duration[row['segment']] += leg_time

        if row['waypoint'] == 'Start':
            if sod:
                day_minutes = 0
                sod = False

        row_dt = (dt.datetime.combine(first_date,
                                      dt.time.fromisoformat(start_time),
                                      ZoneInfo(tzid)
                                      )
                  + dt.timedelta(days=day-1, minutes=day_minutes))
        df.at[index, 'date'] = row_dt.date()
        done_time = row_dt.time()
        ldt = done_time.strftime("%H:%M")
        prev_done_time = done_time
        df.at[index, 'time'] = ldt
        df.at[index, 'pace'] = pace
        df.at[index, 'dt'] = row_dt

        if row['waypoint'] == 'EOD':
            eod_times[day] = done_time
            sod = True
    # END for caltopo_df.iterrowsrow['waypoint']

    return (df,
            eod_times,
            #!dict(day_segments),
            #!pd.DataFrame.from_records([seg_duration]).T,
            )

def deviation_tables(caltopo_df, predictions, start_time,
                     first_date = dt.date.today(),
                     tzid: str = 'America/Phoenix',
                     ):
    """Produce a 2d table for each segment.  Use the first column to
    lookup the deviation betwen Actual segment end time verses the
    Predicted end time.  Then find the column that represents the
    amount you expect the Actual pace for remainder of the day to
    deviate from the Predict pace (in percentage). E.G. 100% means you
    still trust your original Predicted pace for the remainder of the day.
    A column of 50% means you think Actual pace will be 50% of the Predicted pace
    (1/2 the speed you predicted).

    Note: In a day that contains 5 segments, you will get 5 tables.
    The column in the 2nd table will be the hour deviation
    (Predicted-Actual) for the combination of the first two segments.

    """
    pass
