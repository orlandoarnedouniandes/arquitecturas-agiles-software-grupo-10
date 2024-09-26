FROM python:3.10
WORKDIR /detector_actividad_sospechosa

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Make port 3001 available to the world outside this container
EXPOSE 3003

# Define environment variable
ENV FLASK_APP=/app/src/main.py

CMD /bin/bash -c "flask run --host=0.0.0.0 -p 3003"