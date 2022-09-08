
# latest Ubuntu version
FROM ubuntu:latest  AS builder

# information about maintainer
MAINTAINER yves

# add the bash script
ADD Docker/x86/install.sh /runfolder/
ADD /MyExperiments/config /runfolder/config
#ADD Docker/ARM/install.sh /runfolder/

# change rights for the script
RUN chmod u+x /runfolder/install.sh
# run the bash script
RUN /runfolder/install.sh
# prepend the new path
ENV PATH /root/miniconda3/bin:$PATH

#Add enviroment
ADD / /runfolder/

# execute IPython when container is run
#CMD ["ipython"]
# Run Script
RUN chmod u+x /runfolder/config/run.sh
# Run job
CMD /runfolder/config/run.sh
