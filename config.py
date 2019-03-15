import configparser
import os

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'
EXPIRES_AT = 'expires_at'

PATH = "settings.ini"
SECTION_SETTINGS = 'Settings'


def create_config(path=PATH):
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'access_token', '')

    with open(path, 'w') as config_file:
        config.write(config_file)


def get_config(path=PATH):
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(section, setting, path=PATH):
    config = get_config(path)
    value = config.get(section, setting)
    print
    "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value)
    return value


def update_setting(section, setting, value, path=PATH):
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, 'w') as config_file:
        config.write(config_file)


def delete_setting(section, setting, path=PATH):
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, 'w') as config_file:
        config.write(config_file)


def main():
    path = "settings-test.ini"
    update_setting('Settings', 'test', 'a', path)
    get_setting('Settings', 'test', path)
    update_setting('Settings', 'test', 'a', path)
    delete_setting('Settings', 'test', path)


if __name__ == "__main__":
    main()