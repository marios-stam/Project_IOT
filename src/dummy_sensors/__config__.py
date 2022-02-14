SERVER_IP = 'http://localhost:5000/'

# =========== CONSTANTS ===========
ARRAY_SIZE = 30                             # Number of bins in infrastructure
CENTER_POS = {
    'x': 38.288082942215645,
    'y': 21.786401980994090
}                                           # Center position to randomly scatter bins
SCATTER = 0.0175                            # Scatter parameter for positioning arround the center
FILL_RATE = 0.02                            # Fill rate (each interval)
FILL_COVAR = 1.25                           # Variation of fill rate
AMBIENT_TEMP = 25                           # Ambient (starting) temperature
AMBIENT_TEMP_COVAR = 3                      # Variation of ambient temperature
AUTO_DEATH = 2 * 60 * 60 * 24               # Automatically kill process after (seconds)
INTERVAL = 5                                # Interval between measurements (seconds)
FIRE_PERC = 0.0025                          # Chance of bin catching fire (each interval)
FIRE_TEMP = 200                             # Temperature of bin when on fire
FIRE_TEMP_COVAR = 60                        # Variation of temperature when on fire
TILT_PERC = 0.0025                          # Chance of bin being overturned (each interval)
BATTERY_RATE = 0.005                        # Rate at which battery is depleted (each interval)
BATTERY_COVAR = 0.8                         # Variation of battery
MAX_MEASURE_PER_REQ = 10                    # Maximum measurements returned per request
NO_TRASH_CHANCE = 0.075                     # Chance that nobody throws any trash each interval            
STARTS_AT_ZERO = True                       # Start fill level at zero or random percentage
BATTERY_CRITICAL = 0.05                     # Battery level at which sensor stops transmission until charged
