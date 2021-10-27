# Website
 this is a website

## Build
 First build this using: docker build -t flask-tutorial:latest .

## Run
 Then run it by using: docker run -d -p 8000:8000 flask-tutorial
 You can then connect to the Docker Container through the servers IP at port 8000.  I.e. 192.168.1.1:8000
 Note -- The port is 8000 because that is where gunicorn is pointing to in boot.sh.  



