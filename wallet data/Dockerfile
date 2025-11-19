FROM python:3.13.9-slim


# Install pipenv and uvicorn globally
RUN pip install pipenv uvicorn scikit-learn==1.6.1

# Set working directory
WORKDIR /app

# Copy Pipfile
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system --deploy

# Copy app files
COPY main.py wallet_classifer=1.0.bin ./

# Expose port for FastAPI
EXPOSE 9696

# Start uvicorn
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9696"]