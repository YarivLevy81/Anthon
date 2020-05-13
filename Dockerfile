FROM python:3.8-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY Anton Anton
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
CMD ["bash"] 
