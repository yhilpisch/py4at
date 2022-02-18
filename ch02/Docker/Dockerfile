#
# Building a Docker Image with
# the Latest Ubuntu Version and
# Basic Python Install
# 
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

# latest Ubuntu version
FROM ubuntu:latest  AS builder

# information about maintainer
MAINTAINER yves

# add the bash script
ADD /x86/install.sh /runfolder/
#ADD /ARM/install.sh /runfolder/
#Add envorimente
ADD ./MyExperiments /runfolder/
# change rights for the script
RUN chmod u+x /runfolder/install.sh
# run the bash script
RUN /runfolder/install.sh
# prepend the new path
ENV PATH /root/miniconda3/bin:$PATH

# execute IPython when container is run
CMD ["ipython"]
