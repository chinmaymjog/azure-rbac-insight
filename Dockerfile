# Use an official Python runtime as a parent image
FROM python:3.15-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Install into a relocatable prefix so the final stage does not depend on the
# Python minor version (the old hard-coded python3.12 path broke when the base
# image moved to 3.15).
# Floors for transitive dependencies with known HIGH vulnerabilities (Trivy
# image scan) go in the same resolution as requirements.txt. Installing them in a
# second `pip install --prefix` run would leave the old .dist-info behind
# (pip does not see packages in the prefix), and the scanner reports both.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
    "urllib3>=2.8.0" "msgpack>=1.2.3" "setuptools>=78.1.1"

# Final stage
FROM python:3.15-slim

# Apply OS security updates and update setuptools (vulnerable version ships in the base image).
# pip is removed at the end: the app does not need it at runtime, and pip's vendored
# copies of urllib3/msgpack are what the vulnerability scanner reports.
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade "setuptools>=78.1.1" \
    && pip uninstall -y pip

WORKDIR /app

# Copy only the installed packages and entry-point scripts from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
