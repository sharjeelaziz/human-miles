
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
        self.total_meters = 0
        self.last_activity_date = None

        self.sc = stravalib.Client(self.access_token)
        self.start_time = time.time()

    def check_token(self):
        if time.time() > self.expires_at:
            self.access_token = self.sc.refresh_access_token(self.client_id, self.client_secret, self.refresh_token)
            c.update_setting(c.SECTION_SETTINGS, c.ACCESS_TOKEN, str(self.access_token))

    def get_athlete(self):
        self.check_token()
        athlete = self.sc.get_athlete()
        return athlete

    def get_activities(self):
        self.check_token()
        for activity in self.sc.get_activities(after="2019-03-05 22:25:41+00:00"):
            print("{0.name} {0.moving_time} {0.distance} {0.start_date}".format(activity))

    def get_total_distance(self):
        if time.time() > self.start_time:
            self.start_time = time.time() + 900
            self.check_token()
            if self.total_meters == 0:
                for activity in self.sc.get_activities():
                    self.total_meters += float(stravalib.unithelper.miles(activity.distance))
                    if (self.last_activity_date is None) or (activity.start_date > self.last_activity_date):
                        self.last_activity_date = activity.start_date
                    print("First Run: {0.name} {0.moving_time} {0.distance} {0.start_date}".format(activity))

            for activity in self.sc.get_activities(after=self.last_activity_date):
                self.total_meters += float(stravalib.unithelper.miles(activity.distance))
                if (self.last_activity_date is None) or (activity.start_date > self.last_activity_date):
                    self.last_activity_date = activity.start_date
                print("Second Run: {0.name} {0.moving_time} {0.distance} {0.start_date}".format(activity))
        return self.total_meters


def main():
    strava = Strava()
    athlete = strava.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    print(strava.get_total_distance())
    print(strava.get_total_distance())


if __name__ == "__main__":
    main()
