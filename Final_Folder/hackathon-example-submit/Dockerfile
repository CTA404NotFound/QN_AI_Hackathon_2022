# STEP 1: Pull python image
FROM python:3.9.13

# STEP 2,3: CREATE WORK DIR AND COPY FILE TO WORK DIR
WORKDIR /manhpv3_tabai
COPY requirements.txt /manhpv3_tabai

# STEP 4,5,6: INSTALL NECESSARY PACKAGE
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install gdown

# STEP 7: Download file weight
RUN gdown "https://drive.google.com/uc?export=download&id=1VIplhJoaKPI08Qcdq6FhPk_dMvGOfDMp"

# STEP 8: RUN COMMAND
COPY . /manhpv3_tabai
CMD ["python", "./app.py"]