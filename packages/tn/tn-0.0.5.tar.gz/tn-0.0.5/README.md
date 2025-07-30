# tn
Utils to work with time

To install:	```pip install tn```

## Overview
The `tn` package provides a collection of utilities to work with time, especially focusing on conversions between different time units and formats, such as milliseconds, seconds, and datetime objects. It includes functions to handle time zones and to convert between UTC and local times. This package is useful for applications that require precise time manipulation and formatting.

## Features
- Conversion between milliseconds, seconds, nanoseconds, and datetime objects.
- Getting current time in UTC in various units (milliseconds, seconds, nanoseconds).
- Conversion between UTC and local datetime.
- Handling of time zones using `dateutil.tz`.
- Deprecated functions for backward compatibility, raising warnings to encourage the use of updated functions.

## Usage Examples

### Getting Current UTC Time
```python
import tn

# Get current UTC time in seconds
current_utc_seconds = tn.utcnow_timestamp()
print("Current UTC time in seconds:", current_utc_seconds)

# Get current UTC time in milliseconds
current_utc_milliseconds = tn.utcnow_ms()
print("Current UTC time in milliseconds:", current_utc_milliseconds)

# Get current UTC time in nanoseconds
current_utc_nanoseconds = tn.utcnow_ns()
print("Current UTC time in nanoseconds:", current_utc_nanoseconds)
```

### Converting UTC Datetime to Milliseconds
```python
from datetime import datetime
import tn

# Current datetime in UTC
current_datetime_utc = datetime.utcnow()

# Convert UTC datetime to milliseconds
utc_milliseconds = tn.utc_datetime_to_utc_ms(current_datetime_utc)
print("Milliseconds since epoch:", utc_milliseconds)
```

### Converting UTC Milliseconds to Local Datetime
```python
import tn

# Example UTC milliseconds
utc_milliseconds = 1609459200000  # Corresponds to 2021-01-01 00:00:00 UTC

# Convert UTC milliseconds to local datetime
local_datetime = tn.utc_ms_to_local_datetime(utc_milliseconds)
print("Local datetime:", local_datetime)
```

### Time Zone Conversion
```python
from datetime import datetime
import tn

# Current time in UTC
utc_now = datetime.utcnow()

# Convert UTC datetime to local time
local_time = tn.utc_to_local(utc_now)
print("Local time:", local_time)

# Convert local time back to UTC
utc_converted = tn.local_to_utc(local_time)
print("UTC time:", utc_converted)
```

### Working with Days
```python
import tn

# Get milliseconds for the start of the day from a given UTC milliseconds
utc_milliseconds = 1609459200000  # Some example UTC milliseconds
day_start_utc_milliseconds = tn.day_utc_ms_from_utc_ms(utc_milliseconds)
print("Day start in UTC milliseconds:", day_start_utc_milliseconds)

# Convert UTC milliseconds to a datetime object representing start of the day
day_start_datetime = tn.day_datetime_from_utc_ms(utc_milliseconds)
print("Day start datetime:", day_start_datetime)
```

### Formatting Seconds into Minutes and Seconds
```python
import tn

# Example seconds
seconds = 3661  # 1 hour, 1 minute, and 1 second

# Convert seconds to mm:ss format
formatted_time = tn.seconds_to_mmss_str(seconds)
print("Formatted time:", formatted_time)
```

## Function/Class Documentation
- `utcnow_timestamp()`: Returns the current UTC time as a timestamp in seconds since the Unix epoch.
- `utcnow_ms()`: Returns the current UTC time in milliseconds since the Unix epoch.
- `utcnow_ns()`: Returns the current UTC time in nanoseconds since the Unix epoch.
- `utc_datetime_to_utc_ms(utc_datetime)`: Converts a UTC datetime object to milliseconds since the Unix epoch.
- `utc_ms_to_utc_datetime(ums)`: Converts milliseconds since the Unix epoch to a UTC datetime object.
- `utc_ms_to_local_datetime(ums)`: Converts milliseconds since the Unix epoch to a local datetime object.
- `utc_to_local(utc_date)`: Converts a UTC datetime object to local time.
- `local_to_utc(local_date)`: Converts a local datetime object to UTC.
- `day_utc_ms_from_utc_ms(ums)`: Calculates the milliseconds at the start of the day for a given UTC time in milliseconds.
- `day_datetime_from_datetime(date_time)`: Returns a datetime object set to midnight of the day of the provided datetime.
- `day_datetime_from_utc_ms(ums)`: Converts UTC milliseconds to a datetime object representing the start of the day.
- `seconds_to_mmss_str(s)`: Formats a number of seconds into a string in mm:ss format.

## Deprecated Functions
- `unix_time_ms_to_datetime(ums)`: Deprecated. Use `utc_ms_to_local_datetime` instead.
- `datetime_to_unix_time_ms(date)`: Deprecated. Use `utc_datetime_to_utc_ms` instead.

This package is maintained by thor, and aims to provide robust tools for handling and manipulating time data efficiently.