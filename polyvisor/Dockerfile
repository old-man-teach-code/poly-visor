# Use a base image with Python and Node.js
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git npm

# Clone your repository
RUN git clone https://github.com/poly-laboratory/poly-visor.git .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install npm dependencies and build the front-end
RUN npm install
RUN npm run build

# Expose the port on which your Flask app will run
EXPOSE 5000

# Add your application code
COPY . /app

# Start your Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
