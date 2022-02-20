from config import config
from digitalOcean.Run_Droplet import Droplet
import subprocess


# https://www.digitalocean.com/community/tutorials/how-to-use-a-remote-docker-server-to-speed-up-your-workflow
def set_up_droplet_server():
    droplet = Droplet()
    # droplet.Creating_a_new_droplet_with_all_your_SSH_keys()

    #
    user = "root"
    host = droplet.droplet.ip_address # '143.198.239.46'
    command = ['sudo useradd -m -d /home/dockergianni -s /bin/bash dockergianni',
               'sshpass -p {password} ssh {user}@{host}'.format(user=user, host=host, password=config.usr_dockergianni_pw)]
    for cmd in command:
        result = subprocess.Popen("ssh {user}@{host} {cmd}".format(user=user, host=host, cmd=cmd), shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(result)


if __name__ == '__main__':
    set_up_droplet_server()
