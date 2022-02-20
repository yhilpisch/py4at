import digitalocean
from digitalocean import SSHKey
from MyExperiments.config import config


class Droplet(object):
    def __init__(self):
        self.manager = digitalocean.Manager(token=config.digitalocean_token)
        self.droplets = self.manager.get_all_droplets()
        self.droplet = self.droplets[0]

    def Creating_a_new_droplet_with_all_your_SSH_keys(self):
        keys = self.manager.get_all_sshkeys()
        self.droplet = digitalocean.Droplet(token=self.manager.token,
                                            name='BTC-oBT-long',
                                            region='sfo3',  # https://slugs.do-api.dev
                                            image='rancheros',  # https://slugs.do-api.dev
                                            size_slug='s-1vcpu-1gb',  # https://slugs.do-api.dev
                                            ssh_keys=keys,
                                            backups=False)
        m = self.droplet.create()
        print(m)

    def Add_SSHKey_into_DigitalOcean_Account(self):
        user_ssh_key = open('/Users/hans/.ssh/public_lette.pub').read()
        key = SSHKey(token=self.manager.token,
                     name=self.droplet.name,
                     public_key=user_ssh_key)
        m = key.create()
        print(m)

    def Checking_the_status_of_the_droplet(self):
        if self.droplet is None:
            my_droplets = self.manager.get_all_droplets()
            self.droplet = self.droplet
        actions = self.droplet.get_actions()
        for action in actions:
            action.load()
            # Once it shows "completed", droplet is up and running
            print(action.status)


if __name__ == '__main__':
    droplet = Droplet()
    droplet.Add_SSHKey_into_DigitalOcean_Account()
    #droplet.Creating_a_new_droplet_with_all_your_SSH_keys()
    #droplet.Checking_the_status_of_the_droplet()