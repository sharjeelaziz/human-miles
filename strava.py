
import stravalib
import time
import config as c


class Strava(object):

    def __init__(self):
        self.client_id = c.get_setting(c.SECTION_SETTINGS, c.CLIENT_ID)
        self.client_secret = c.get_setting(c.SECTION_SETTINGS, c.CLIENT_SECRET)

        self.access_token = c.get_setting(c.SECTION_SETTINGS, c.ACCESS_TOKEN)
        self.refresh_token = c.get_setting(c.SECTION_SETTINGS, c.REFRESH_TOKEN)
        self.expires_at = float(c.get_setting(c.SECTION_SETTINGS, c.EXPIRES_AT))

        self.sc = stravalib.Client(self.access_token)

    def check_token(self):
        if time.time() > self.expires_at:
            self.access_token = self.sc.refresh_access_token(self.client_id, self.client_secret, self.refresh_token)

    def get_athlete(self):
        self.check_token()
        athlete = self.sc.get_athlete()
        return athlete

    def get_activities(self):
        for activity in self.sc.get_activities(after="2019-03-05 22:25:41+00:00"):
            print("{0.name} {0.moving_time} {0.distance} {0.start_date}".format(activity))


def main():
    strava = Strava()
    athlete = strava.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    strava.get_activities()


if __name__ == "__main__":
    main()
