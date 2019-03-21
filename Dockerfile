FROM python:3
ADD app.py /
ADD serviceAccountKey.json /
RUN pip install pyrebase
RUN pip install argparse
RUN pip install google-cloud-firestore
RUN pip install firebase_admin
CMD ["python", "./app.py"]
