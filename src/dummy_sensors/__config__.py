SERVER_IP = 'http://31.208.108.233:5000/'

# =========== CONSTANTS ===========
ARRAY_SIZE = 5                              # Number of bins in infrastructure
CENTER_POS = {
    'x': 38.246639,
    'y': 21.734573
}                                           # Center position to randomly scatter bins
FILL_RATE = 0.05                            # Fill rate (each interval)
AMBIENT_TEMP = 25                           # Ambient (starting) temperature
AUTO_DEATH = 2 * 60 * 60 * 24               # Automatically kill process after (seconds)
INTERVAL = 5                                # Interval between measurements (seconds)
FIRE_PERC = 0.005                           # Chance of bin catching fire (each interval)
FIRE_TEMP = 135                             # Temperature of bin when on fire
TILT_PERC = 0.005                           # Chance of bin being overturned (each interval)
BATTERY_RATE = 0.007                        # Rate at which battery is depleted (each interval)
MAX_MEASURE_PER_REQ = 10                    # Maximum measurements returned per request
