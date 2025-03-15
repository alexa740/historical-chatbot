# Use a base Python image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install system dependencies for FAISS
RUN apt-get update && apt-get install -y libfaiss-dev libfaiss-avx2

# Install required Python libraries
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for Streamlit
EXPOSE 7860

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
