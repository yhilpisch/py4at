import subprocess
import sys
import time

import docker

from digitalOcean import config
from digitalOcean.Droplet import Droplet

def build_docker():
    ssh_client = docker.DockerClient(base_url="ssh://root@{host}".format(host='gellos.games'))
    image, build_logs = ssh_client.images.build(path=sys.path[2], tag='backtest', rm=True)  # Error by: , tag='BTC_BackTest_long_py', rm=False
    for line in build_logs:
        print(line)

    container = ssh_client.containers.run("backtest", detach=True)
    for line in container.logs(stream=True):
        print(line.strip())
    print("build-done")



if __name__ == '__main__':
    build_docker()
    print("Done")
    # Not working because of an issue https://github.com/fabric/fabric/issues/2182