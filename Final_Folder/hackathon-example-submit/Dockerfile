# STEP 1: Pull python image
FROM python:3.9.13

# STEP 2,3: CREATE WORK DIR AND COPY FILE TO WORK DIR
WORKDIR /cta404notfound
COPY requirements.txt /cta404notfound

# STEP 4,5,6: INSTALL NECESSARY PACKAGE
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install gdown

# STEP 7: Download file weight
RUN gdown "https://drive.google.com/file/d/1Z673t-kcZM8YwC0v14zLx80W1UP-DHIe/view?usp=sharing"
#Download file stop word
RUN gdown "https://drive.google.com/file/d/1nbKTtYPgHCwCIPObsuyyaYgH6a0JJ8pZ/view?usp=sharing"
#Download file vncorenlp folder
RUN gdown "https://drive.google.com/drive/folders/17gNuoKfOC02q57Qux0COG3Q_sFheAYja?usp=sharing"

# STEP 8: RUN COMMAND
COPY . /cta404notfound
CMD ["python", "./app.py"]