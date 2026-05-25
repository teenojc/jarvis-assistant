"""Timezone Utilities for Digital Clock"""

import pytz
from datetime import datetime, timedelta
from loguru import logger


class TimezoneUtils:
    """Utility functions for timezone operations"""
    
    @staticmethod
    def search_timezone(query):
        """Search for timezone by name"""
        query = query.lower()
        results = [tz for tz in pytz.all_timezones if query in tz.lower()]
        logger.info(f"Search found {len(results)} timezones")
        return results
    
    @staticmethod
    def get_current_utc_offset(timezone):
        """Get current UTC offset for timezone"""
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            offset = now.strftime("%z")
            hours = int(offset[:3])
            minutes = int(offset[3:5])
            
            return {
                'timezone': timezone,
                'offset_hours': hours,
                'offset_minutes': minutes,
                'offset_string': f"UTC{offset[:3]}:{offset[3:5]}",
                'is_dst': bool(now.dst())
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    @staticmethod
    def get_next_dst_change(timezone):
        """Get next daylight saving time change"""
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            
            for i in range(1, 366):
                future = now + timedelta(days=i)
                future_tz = tz.localize(future.replace(tzinfo=None))
                
                if future_tz.dst() != now.dst():
                    return {
                        'timezone': timezone,
                        'current_dst': bool(now.dst()),
                        'next_change_date': future_tz.strftime("%Y-%m-%d"),
                        'days_until_change': i
                    }
            
            return {'timezone': timezone, 'next_change': 'Not found in next year'}
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    @staticmethod
    def get_time_diff_hours(tz1, tz2):
        """Get hour difference between two timezones"""
        try:
            now = datetime.now(pytz.UTC)
            time1 = now.astimezone(pytz.timezone(tz1))
            time2 = now.astimezone(pytz.timezone(tz2))
            
            diff = (time1.utcoffset() - time2.utcoffset()).total_seconds() / 3600
            return diff
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    @staticmethod
    def is_valid_timezone(timezone):
        """Check if timezone string is valid"""
        try:
            pytz.timezone(timezone)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    @staticmethod
    def get_nearby_timezones(timezone, hour_offset_range=2):
        """Get timezones near the given one by UTC offset"""
        try:
            target_tz = pytz.timezone(timezone)
            target_offset = datetime.now(target_tz).utcoffset().total_seconds() / 3600
            
            nearby = []
            for tz in pytz.all_timezones:
                tz_obj = pytz.timezone(tz)
                tz_offset = datetime.now(tz_obj).utcoffset().total_seconds() / 3600
                
                if abs(tz_offset - target_offset) <= hour_offset_range:
                    nearby.append(tz)
            
            return nearby
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
