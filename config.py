import yaml

y_file = './resource/application-dev.yml'

with open(y_file, 'r') as yml:
    cfg = yaml.safe_load(yml)

class TargetConfig:
    FINANCE = cfg['URL']['FINANCE']
    DB_HOST = cfg['DB']['HOST']
    DB_USER = cfg['DB']['USER']
    DB_PW = cfg['DB']['PW']
    DB_NAME = cfg['DB']['DB']