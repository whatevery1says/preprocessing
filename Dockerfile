FROM jupyter/datascience-notebook:177037d09156

LABEL maintainer="Jeremy Douglass <jeremydouglass@gmail.com>" \
      description="we1s-notebook, a Jupyter datascience notebook for WE1S"

# Build:
#   docker build -t jeremydouglass/preprocessing --build-arg CACHE_DATE="$(date)"
# Run:
#   docker run -p 8888:8888 jeremydouglass/preprocessing

# Java

ENV JAVA_HOME="/opt/conda/pkgs/openjdk-8.0.144-zulu8.23.0.3_1" \
    LD_LIBRARY_PATH="/opt/conda/pkgs/openjdk-8.0.144-zulu8.23.0.3_1/jre/lib/amd64/server/"
USER $NB_UID
RUN conda install -c conda-forge \
    'openjdk=8.0.144'

# ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
# USER root
# # Add proper open-jdk-8 not just the jre, needed for pydoop
# RUN echo 'deb http://cdn-fastly.deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list && \
#     apt-get -y update && \
#     apt-get install --no-install-recommends -t jessie-backports -y openjdk-8-jdk && \
#     rm /etc/apt/sources.list.d/jessie-backports.list && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/ && \


# MALLET

WORKDIR /home/jovyan
USER root
RUN wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip \
 && unzip mallet-2.0.8.zip \
 && rm mallet-2.0.8.zip
ENV PATH="/home/jovyan/mallet-2.0.8/bin:${PATH}" \
    MALLET_HOME="/home/jovyan/mallet-2.0.8/bin"


# shell

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    zip=3.0-11build1 \
    libfuzzy-dev \
    ssdeep \
 && ln -s /bin/tar /bin/gtar \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*	


# Python

USER $NB_UID
RUN conda install -c anaconda \
    'unidecode=1.0.22' \
    'natsort=5.3.3' \
    'ftfy=5.5.1' \
    'nltk==3.4.1'
RUN conda install -c conda-forge \
    'fire=0.1.3' \
    'numpy==1.16.3' \
    'pandas==0.23.4' \
    'pyldavis=2.1.2'
RUN conda install -c conda-forge \
    'spacy==2.1.3'
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md

RUN pip install --upgrade pip

##################
#  IMPORT TOOLS  #
##################

USER root
WORKDIR /home/jovyan/utils/
RUN chown -R 1000:100 /home/jovyan/utils

# Approach 1: copy the Dockerfile repo in directly
COPY --chown=1000:100 . /home/jovyan/utils/preprocessing

# Approach 2: create a git repo, for a commit sandbox
WORKDIR /home/jovyan/utils/preprocessing-git
RUN chown -R 1000:100 /home/jovyan/utils/preprocessing-git
USER $NB_UID
# git clone manual cache-buster, use to bust cache
# even though changes in git clone cannot be detected
# use with:
#   docker build -t jeremydouglass/preprocessing --build-arg CACHE_DATE="$(date)"
# as per https://github.com/moby/moby/issues/1996#issuecomment-465230472
ARG CACHE_DATE=0
RUN git clone -b clean https://github.com/whatevery1says/preprocessing.git .


USER $NB_UID
RUN pip install -r requirements.txt

WORKDIR /home/jovyan
# ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
