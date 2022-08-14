# STEP 1: Pull python image
FROM python:3.9.13

# STEP 2,3: CREATE WORK DIR AND COPY FILE TO WORK DIR
WORKDIR /cta404notfound
COPY requirements.txt /cta404notfound

# STEP 4,5,6: INSTALL NECESSARY PACKAGE
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install gdown

# # Install OpenJDK-11
# RUN apt-get update && \
#     apt-get install -y openjdk-11-jre-headless && \
#     apt-get clean;

# STEP 7: Download file weight

RUN gdown "https://drive.google.com/u/0/uc?id=1Z673t-kcZM8YwC0v14zLx80W1UP-DHIe&export=download"

RUN gdown "https://drive.google.com/u/0/uc?id=1Z673t-kcZM8YwC0v14zLx80W1UP-DHIe&export=download"

#Download file stop word
RUN gdown "https://drive.google.com/u/6/uc?id=1nbKTtYPgHCwCIPObsuyyaYgH6a0JJ8pZ&export=download"



# STEP 8: RUN COMMAND
COPY . /cta404notfound
CMD ["python", "./app.py"]