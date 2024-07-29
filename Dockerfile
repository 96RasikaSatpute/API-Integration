FROM google/cloud-sdk

# Specifying my e-mail address as the maintainer of the container image
LABEL maintainer="rsatpute@pdx.edu"

# Copying the contents of the current directory into the container directory /app
COPY . /app

# Setting up the working directory of the container to /app
WORKDIR /app

# Installing the Python packages as mentioned by requirements.txt in the container
RUN apt update -y && apt install -y python3-pip && pip3 install -r requirements.txt

# Parameters to the program settled up
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

