from yaml import load


class Config:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            init_config = load(f)
        self.username = init_config['config']['crabgrass']['username']
        self.password = init_config['config']['crabgrass']['password']
        self.group = init_config['config']['crabgrass']['group']
        self.url = init_config['config']['crabgrass']['url']
        self.uri_me = init_config['config']['crabgrass']['uri']['me']
        self.uri_pages = init_config['config']['crabgrass']['uri']['pages']
        self.dir_backup = init_config['config']['directories']['backup']
