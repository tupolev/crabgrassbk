from yaml import load


class Config:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            init_config = load(f)
        self.phantomjs_bin_path = init_config['config']['phantomjs']['path']
        self.username = init_config['config']['crabgrass']['username']
        self.password = init_config['config']['crabgrass']['password']
        self.group = init_config['config']['crabgrass']['group']
        self.url = init_config['config']['crabgrass']['url']
        self.uri_me = init_config['config']['crabgrass']['uri']['me']
        self.uri_pages = init_config['config']['crabgrass']['uri']['pages']
        self.dir_backup = init_config['config']['directories']['backup']
        self.subdir_images = init_config['config']['directories']['images_sub_dir']
        self.subdir_attachments = init_config['config']['directories']['attachments_sub_dir']
        self.not_downloadable_extensions = init_config['config']['not_downloadable_extensions']
        self.download_images = init_config['config']['download_images']
        self.download_attachments = init_config['config']['download_attachments']
