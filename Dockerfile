FROM ubuntu:18.04 


RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY ./requirements.txt requirements.txt
COPY ./ /opt/


RUN pip3 install -r requirements.txt 
WORKDIR /opt/


EXPOSE 5001
#ENTRYPOINT [ "python3" ] 
#CMD ["run.py"]
CMD ["gunicorn3","-b","0.0.0.0:5001","run:app"]

