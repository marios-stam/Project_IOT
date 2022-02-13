SERVER_IP = 'http://localhost:5000/'

# =========== CONSTANTS ===========
ARRAY_SIZE = 5                              # Number of bins in infrastructure
CENTER_POS = {
    'x': 38.288082942215645,
    'y': 21.78640198099409
}                                           # Center position to randomly scatter bins
SCATTER = 0.0175                            # Scatter parameter for positioning arround the center
FILL_RATE = 0.01                            # Fill rate (each interval)
AMBIENT_TEMP = 25                           # Ambient (starting) temperature
AUTO_DEATH = 2 * 60 * 60 * 24               # Automatically kill process after (seconds)
INTERVAL = 30                               # Interval between measurements (seconds)
FIRE_PERC = 0.0025                          # Chance of bin catching fire (each interval)
FIRE_TEMP = 135                             # Temperature of bin when on fire
TILT_PERC = 0.0025                          # Chance of bin being overturned (each interval)
BATTERY_RATE = 0.005                        # Rate at which battery is depleted (each interval)
MAX_MEASURE_PER_REQ = 10                    # Maximum measurements returned per request
NO_TRASH_CHANCE = 0.05                      # Chance that nobody throws any trash each interval            
STARTS_AT_ZERO = True                       # Start fill level at zero or random percentage
BATTERY_CRITICAL = 0.05                     # Battery level at which sensor stops transmission until charged