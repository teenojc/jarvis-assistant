"""Digital Clock Core Module"""

import pytz
from datetime import datetime
from loguru import logger


class DigitalClock:
    """Manage digital clock with timezone support"""
    
    def __init__(self):
        """Initialize digital clock"""
        logger.info("Initializing Digital Clock")
        self.timezones = {}
        self.format_24h = True
    
    def get_current_time(self, timezone='UTC'):
        """Get current time in specified timezone"""
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            logger.info(f"Current time in {timezone}: {now}")
            return now
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def get_time_with_timezone(self, timezone='UTC', format_24h=True):
        """Get time with timezone info"""
        now = self.get_current_time(timezone)
        if not now:
            return None
        
        if format_24h:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%I:%M:%S %p")
        
        tz_offset = now.strftime("%z")
        
        return {
            'timezone': timezone,
            'time': time_str,
            'date': now.strftime("%Y-%m-%d"),
            'day': now.strftime("%A"),
            'offset': tz_offset,
            'unix_timestamp': int(now.timestamp())
        }
    
    def add_timezone(self, name, timezone):
        """Add a timezone to display"""
        if not self.is_valid_timezone(timezone):
            logger.error(f"Invalid timezone: {timezone}")
            return False
        
        self.timezones[name] = timezone
        logger.info(f"Timezone added: {name} -> {timezone}")
        return True
    
    def remove_timezone(self, name):
        """Remove a timezone from display"""
        if name in self.timezones:
            del self.timezones[name]
            logger.info(f"Timezone removed: {name}")
            return True
        return False
    
    def get_all_timezones_time(self, format_24h=True):
        """Get current time for all added timezones"""
        times = {}
        for name, timezone in self.timezones.items():
            time_data = self.get_time_with_timezone(timezone, format_24h)
            if time_data:
                times[name] = time_data
        
        logger.info(f"Retrieved times for {len(times)} timezones")
        return times
    
    def is_valid_timezone(self, timezone):
        """Check if timezone is valid"""
        try:
            pytz.timezone(timezone)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    def search_timezones(self, query):
        """Search for timezones matching query"""
        query = query.lower()
        matching = [tz for tz in pytz.all_timezones if query in tz.lower()]
        logger.info(f"Found {len(matching)} timezones matching '{query}'")
        return matching
    
    def get_time_difference(self, tz1, tz2):
        """Get time difference between two timezones"""
        try:
            time1 = self.get_current_time(tz1)
            time2 = self.get_current_time(tz2)
            
            if not time1 or not time2:
                return None
            
            diff = abs((time1.utcoffset() - time2.utcoffset()).total_seconds() / 3600)
            logger.info(f"Time difference: {diff} hours")
            return diff
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def convert_time(self, time_str, from_tz, to_tz, format_24h=True):
        """Convert time from one timezone to another"""
        try:
            from_timezone = pytz.timezone(from_tz)
            to_timezone = pytz.timezone(to_tz)
            
            from_time = datetime.strptime(time_str, "%H:%M:%S" if len(time_str.split(':')) == 3 else "%H:%M")
            localized_time = from_timezone.localize(from_time)
            converted_time = localized_time.astimezone(to_timezone)
            
            if format_24h:
                result = converted_time.strftime("%H:%M:%S")
            else:
                result = converted_time.strftime("%I:%M:%S %p")
            
            logger.info(f"Converted {time_str}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
