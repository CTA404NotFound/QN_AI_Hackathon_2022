# STEP 1: Pull python image
FROM python:3.9.13

# STEP 2,3: CREATE WORK DIR AND COPY FILE TO WORK DIR
WORKDIR /cta404notfound
COPY requirements.txt /cta404notfound

# STEP 4,5,6: INSTALL NECESSARY PACKAGE
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install gdown

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

#Download file stop word
RUN gdown "https://drive.google.com/u/6/uc?id=1nbKTtYPgHCwCIPObsuyyaYgH6a0JJ8pZ&export=download"

# STEP 7: Download file weight
RUN mkdir -p /cta404notfound/Weight_Model
RUN cd /cta404notfound/Weight_Model && gdown "https://drive.google.com/uc?export=download&id=1-8jLQR4RTUn7qNnMRsgVKAC-Bk07K9xR" && gdown "https://drive.google.com/uc?export=download&id=1NIsxMCbEHT2yD6Be4LxXKYOtOP3aByIl"

# ADD Weight_Model /cta404notfound
# #install vncorenlp folder
# RUN yum install unzip
# ADD vncorenlp.zip /cta404notfound/
# RUN cd /cta404notfound && unzip vncorenlp.zip && rm vncorenlp.zip

# STEP 8: RUN COMMAND
COPY . /cta404notfound
CMD ["python", "./app.py"]