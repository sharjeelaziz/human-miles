import strava
import datetime
import time
from microdotphat import set_brightness, write_string, set_decimal, clear, show

st = strava.Strava()

set_brightness(0.1)

while True:
    clear()

    t = datetime.datetime.now()

    if t.second > 10:
        if t.second % 2 == 0:
            set_decimal(2, 1)
            set_decimal(4, 1)
        else:
            set_decimal(2, 0)
            set_decimal(4, 0)
        write_string(t.strftime("%H%M%S"), kerning=False)
    else:
        total_distance = "{:6.0f}".format(st.get_total_distance())
        write_string(total_distance, kerning=False)

    show()
    time.sleep(1)
