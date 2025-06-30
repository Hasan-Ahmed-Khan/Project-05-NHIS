
# Use the official Python image as a base
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy model and requirements
COPY models/satisfaction_prediction_model.joblib /app/model.joblib
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy prediction script
COPY predict.py /app/

# Expose port for the API
EXPOSE 5000

# Run the API
CMD ["python", "predict.py"]
