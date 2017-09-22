# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
# (c) Copyright 2017 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import datetime


def str_to_num(val):
    # if val is a number then convert it to a number literal
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except:   # noqa
            return val


def timestamp(dt=None,
              epoch=datetime.datetime(1970, 1, 1),
              allow_microseconds=False):
    """
    Return a timestamp in seconds since epoch.

    We normalize the timestamps to second precision since python2 cant do
    microseconds properly.
    Setting allow_microseconds=True will return them whenever possible
    but will make timestamps from different python versions inconsistent.

    This function assumes that all machines are configured with the same
    timezone.

    Passing in a epoch that has tz_info set will cause the timestamp to be TZ
    aware for python 2-3.2. Example:
        ts = timestamp(datetime.datetime(1970, 1, 1, tzinfo=timezone))
    To get a TZ aware timestamp for python 3.3+ you must pass in a
    datetime that has tz_info set. Example:
        dt = datetime.datetime.now().replace(tz_info=timezone)
        ts = timestamp(dt)

    In both cases timezone must be an implementation of the abstract base class
    datetime.tzinfo
    """
    if dt is None:
        dt = datetime.datetime.now()

    try:
        # Python 3.3+
        ts = dt.timestamp()
    except AttributeError:
        try:
            # Python 3.0-3.2
            # timedelta supports division
            ts = (dt - epoch) / datetime.timedelta(seconds=1)
        except TypeError:
            # Python 2
            ts = (dt - epoch).total_seconds()

    if allow_microseconds:
        return ts
    else:
        return int(ts)


def _formatter(start, end):
    if start == end:
        return str(start)
    return '{}-{}'.format(start, end)


def string_range(seq):
    """
    Formats the list into readable format
    Ex : [1,2,3,5,6,7] to 1-3,5-7
    """
    if len(seq) == 0:
        return ''
    if len(seq) == 1:
        return str(seq[0])
    result = []
    prev = seq[0]
    seq_start = seq[0]
    for i in seq[1:]:
        # Step size for truncation is 1
        if i - prev != 1:
            result.append(_formatter(seq_start, prev))
            seq_start = i
        # Handle the last entry of the list
        if i == seq[-1]:
            result.append(_formatter(seq_start, i))
        prev = i
    return ','.join(result)
