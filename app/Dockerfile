FROM alpine:latest

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip3 install --upgrade pip

EXPOSE 8080

WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip3 --no-cache-dir install -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
CMD ["python3", "app.py"]
