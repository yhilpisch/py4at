import digitalocean
from digitalocean import SSHKey
from digitalOcean import config


class Droplet(object):
    droplets = None
    manager = digitalocean.Manager(token=config.digitalocean_token)

    def __init__(self):
        self.droplet = None

    def creating_a_new_droplet_with_all_your_SSH_keys(self):
        keys = self.manager.get_all_sshkeys()
        self.droplet = digitalocean.Droplet(token=self.manager.token,
                                            name='BTC-oBT-long',
                                            region='sfo3',  # https://slugs.do-api.dev
                                            image='docker-20-04',  # https://slugs.do-api.dev
                                            size_slug='c-32',  # https://slugs.do-api.dev
                                            ssh_keys=keys,
                                            backups=False)
        m = self.droplet.create()
        print(m)

    def add_SSHKey_into_DigitalOcean_Account(self):
        user_ssh_key = open('/Users/hans/.ssh/public_lette.pub').read()
        key = SSHKey(token=self.manager.token,
                     name=self.droplet.name,
                     public_key=user_ssh_key)
        m = key.create()
        print(m)

    def checking_the_status_of_the_droplet(self):
        if self.droplet is None:
            my_droplets = self.manager.get_all_droplets()
            self.droplet = self.droplet
        actions = self.droplet.get_actions()
        for action in actions:
            action.load()
            # Once it shows "completed", droplet is up and running
            print(action.status)

    def destroy_droplet(self):
        # self.droplet.shutdown()  # cos still costs if it just turned off
        if not self.droplet.destroy():
            raise InterruptedError("Could not destroy Server")

    @staticmethod
    def destroy_all_droplets():
        for drop in Droplet.manager.get_all_droplets():
            if not drop.destroy():
                raise InterruptedError("Could not destroy Server")

    @staticmethod
    def get_all_droplets():
        Droplet.droplets = Droplet.manager.get_all_droplets()
        return Droplet.droplets


if __name__ == '__main__':
    ll = Droplet.get_all_droplets()

    #droplet = Droplet()
    #droplet.droplet = ll[1]
    Droplet.destroy_all_droplets()

    print("dd")
