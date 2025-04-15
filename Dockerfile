# Use the latest small Ubuntu-based GDAL image from OSGeo
FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

# Add the deadsnakes PPA to get Python 3.11
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv build-essential \
    libpq-dev gdal-bin libgdal-dev libgeos-dev libproj-dev && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory to /app
WORKDIR /app

# Create a virtual environment with Python 3.11
RUN python3.11 -m venv /app/venv


# Activate the virtual environment and install dependencies
COPY requirements.txt .
RUN /app/venv/bin/pip install -i https://m.devpi.net/jaraco/dev suds-jurko && \
    /app/venv/bin/pip install -r requirements.txt

# Ensure the virtual environment is used for future commands
ENV PATH="/app/venv/bin:$PATH"


# environment variables for static assets and templates
ENV STATIC_FOLDER=static
ENV TEMPLATES_FOLDER=templates
ENV COMPRESSOR_DEBUG=COMPRESSOR_DEBUG
ENV DOCKER_BUILDKIT=0
ENV DASH_PROD=True


ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

# copy files
COPY application.py /app
COPY data_loader.py /app
# COPY config.py /app
# COPY .ebextensions /app/.ebextensions

# copy data folder into /app
COPY assets /app/assets
COPY data /app/data
COPY figures /app/figures
COPY layouts /app/layouts
COPY pages /app/pages

# Expose port
EXPOSE 10000

# Run application
CMD ["python3", "application.py"]

