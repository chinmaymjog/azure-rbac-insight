# Use an official Python runtime as a parent image
FROM python:3.15-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Install into a relocatable prefix so the final stage does not depend on the
# Python minor version (the old hard-coded python3.12 path broke when the base
# image moved to 3.15).
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.15-slim

WORKDIR /app

# Copy only the installed packages and entry-point scripts from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
