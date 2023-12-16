# Use an official Python runtime as a base image
FROM python:3.8-slim as build

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    npm

# Clone the Polyvisor repository
RUN git clone https://github.com/poly-laboratory/poly-visor.git

# Change the working directory to /app/poly-visor
WORKDIR /app/poly-visor

# Install npm dependencies for front-end and build to production
RUN npm install
RUN npm run build

# Install Polyvisor via pip
RUN pip install .

# Create a new stage for the final image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the built files from the previous stage
COPY --from=build /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build /app/poly-visor /app/poly-visor

# Set the environment variables
ENV PATH="/app/poly-visor:${PATH}"

# Expose the required port for Polyvisor
EXPOSE 5000

# Start Polyvisor with supervisord
CMD ["supervisord", "-c", "/app/poly-visor/supervisord.conf"]