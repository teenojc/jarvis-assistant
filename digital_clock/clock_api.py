"""Flask API for Digital Clock"""

from flask import Flask, jsonify, request
from loguru import logger
from digital_clock.clock import DigitalClock
from digital_clock.timezone_utils import TimezoneUtils
from datetime import datetime

app = Flask(__name__)
clock = DigitalClock()

# Initialize with common timezones
common_tzs = {
    'New York': 'America/New_York',
    'London': 'Europe/London',
    'Tokyo': 'Asia/Tokyo',
    'Sydney': 'Australia/Sydney',
    'Dubai': 'Asia/Dubai',
}

for name, tz in common_tzs.items():
    clock.add_timezone(name, tz)

logger.info("Digital Clock API initialized")


@app.route('/api/current-time', methods=['GET'])
def get_current_time():
    """Get current time in specified timezone"""
    timezone = request.args.get('timezone', 'UTC')
    format_24h = request.args.get('format', 'true').lower() == 'true'
    
    time_data = clock.get_time_with_timezone(timezone, format_24h)
    
    if time_data:
        logger.info(f"Returning time for: {timezone}")
        return jsonify(time_data)
    else:
        return jsonify({'error': 'Invalid timezone'}), 400


@app.route('/api/all-timezones-time', methods=['GET'])
def get_all_timezones_time():
    """Get current time for all added timezones"""
    format_24h = request.args.get('format', 'true').lower() == 'true'
    times = clock.get_all_timezones_time(format_24h)
    logger.info(f"Returning times for {len(times)} timezones")
    return jsonify(times)


@app.route('/api/add-timezone', methods=['POST'])
def add_timezone():
    """Add a new timezone"""
    data = request.json
    name = data.get('name')
    timezone = data.get('timezone')
    
    if not name or not timezone:
        return jsonify({'error': 'Missing parameters'}), 400
    
    success = clock.add_timezone(name, timezone)
    
    if success:
        logger.info(f"Timezone added: {name}")
        return jsonify({'success': True, 'message': f'Timezone {name} added'})
    else:
        return jsonify({'error': 'Invalid timezone'}), 400


@app.route('/api/remove-timezone/<name>', methods=['DELETE'])
def remove_timezone(name):
    """Remove a timezone"""
    success = clock.remove_timezone(name)
    
    if success:
        logger.info(f"Timezone removed: {name}")
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Not found'}), 404


@app.route('/api/search-timezones', methods=['GET'])
def search_timezones():
    """Search for timezones"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Missing query'}), 400
    
    results = TimezoneUtils.search_timezone(query)
    logger.info(f"Search results: {len(results)} found")
    return jsonify({'results': results})


@app.route('/api/convert-time', methods=['GET'])
def convert_time():
    """Convert time between timezones"""
    time_str = request.args.get('time')
    from_tz = request.args.get('from')
    to_tz = request.args.get('to')
    format_24h = request.args.get('format', 'true').lower() == 'true'
    
    if not time_str or not from_tz or not to_tz:
        return jsonify({'error': 'Missing parameters'}), 400
    
    result = clock.convert_time(time_str, from_tz, to_tz, format_24h)
    
    if result:
        logger.info(f"Converted: {result}")
        return jsonify({'converted_time': result, 'from': from_tz, 'to': to_tz})
    else:
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/api/time-difference', methods=['GET'])
def get_time_difference():
    """Get time difference between timezones"""
    tz1 = request.args.get('tz1')
    tz2 = request.args.get('tz2')
    
    if not tz1 or not tz2:
        return jsonify({'error': 'Missing parameters'}), 400
    
    diff = clock.get_time_difference(tz1, tz2)
    
    if diff is not None:
        return jsonify({'difference_hours': diff, 'tz1': tz1, 'tz2': tz2})
    else:
        return jsonify({'error': 'Invalid timezone'}), 400


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Digital Clock API',
        'timestamp': datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    logger.info("Starting Digital Clock API")
    app.run(debug=True, host='0.0.0.0', port=5000)
