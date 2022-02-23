import subprocess
import sys
import time

import docker

from digitalOcean import config
from digitalOcean.Droplet import Droplet


# https://www.digitalocean.com/community/tutorials/how-to-use-a-remote-docker-server-to-speed-up-your-workflow
def set_up_droplet_server():
    new_droplet = Droplet()
    new_droplet.creating_a_new_droplet_with_all_your_SSH_keys()
    # Wait for creating vServer
    while new_droplet.droplet.ip_address is None:
        time.sleep(90)

    print(new_droplet.droplet.ip_address)
    return new_droplet


def create_user(server):
    #
    user = "root"
    host = server.droplet.ip_address  # '143.198.239.46'
    command = ['sudo useradd -m -d /home/dockergianni -s /bin/bash dockergianni',
               'sshpass -p {password} ssh {user}@{host}'.format(user=user, host=host,
                                                                password=config.usr_dockergianni_pw)]
    for cmd in command:
        result = subprocess.Popen("ssh {user}@{host} {cmd}".format(user=user, host=host, cmd=cmd), shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(result)

def build_docker(drop):
    ssh_client = docker.DockerClient(base_url="ssh://root@{host}".format(host=drop.ip_address))
    image, build_logs = ssh_client.images.build(path=sys.path[2], tag='backtest', rm=False)  # Error by: , tag='BTC_BackTest_long_py', rm=False
    for line in build_logs:
        print(line)

    container = ssh_client.containers.run("backtest", detach=True)
    for line in container.logs(stream=True):
        print(line.strip())
    print("dd")


if __name__ == '__main__':
    #drop = set_up_droplet_server()
    drop =  Droplet.get_all_droplets()[0]
    print(drop.ip_address)
    #create_user(drop)
    build_docker(drop)
    print("ee")


