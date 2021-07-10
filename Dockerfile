FROM ubuntu
RUN apt-get -y update
RUN apt-get install python3 python3-pip -y
WORKDIR /app
COPY /requeriments.txt /app
RUN pip3 install -r requeriments.txt
COPY ["src/script.py", "/app"]
EXPOSE 5001
ENTRYPOINT ["python3"]
CMD ["script.py"]
