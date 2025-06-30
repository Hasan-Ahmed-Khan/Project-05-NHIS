# TellCo Telecom User Analytics Project

## Project Overview
This project analyzes TellCo's telecommunications dataset to evaluate business opportunities and make data-driven recommendations for potential acquisition. The analysis is divided into four main sections focusing on user behavior, engagement, experience, and satisfaction.

## Setup Instructions

### Prerequisites
- Python 3.6+
- MySQL (optional, for database export)
- Docker (optional, for model deployment)

### Installation
1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Place the telecom dataset in the `data/` directory as `telcom_data.csv`

## Project Structure
- `analysis.ipynb`: Main Jupyter notebook containing all analysis
- `data/`: Directory containing the telecom dataset
- `models/`: Directory for storing trained ML models and artifacts
- `Dockerfile`: Configuration for containerizing the ML model
- `predict.py`: API script for serving model predictions

## Analysis Components

### 1. User Overview Analysis
- Handset analysis (top manufacturers and models)
- Application usage patterns
- Data traffic analysis per application
- Exploratory data analysis

### 2. User Engagement Analysis
- Session frequency, duration, and traffic metrics
- Clustering of users based on engagement patterns
- Top engaged users identification

### 3. User Experience Analysis
- Network performance metrics (TCP retransmission, RTT, throughput)
- Experience metrics by handset type
- Clustering of users based on experience quality

### 4. User Satisfaction Analysis
- Engagement score calculation using Euclidean distance from least engaged cluster
- Experience score calculation using Euclidean distance from worst experience cluster
- Satisfaction score as average of engagement and experience scores
- Regression modeling to predict satisfaction
- Customer segmentation (k-means) based on satisfaction metrics
- Model deployment with tracking (MLflow)
- Data export to MySQL/CSV

## Model Deployment with Docker

The project includes a containerized deployment of the satisfaction prediction model using Docker. This enables consistent deployment across different environments and simplifies the deployment process.

### Prerequisites for Docker Deployment
- Docker installed on your system ([Docker Installation Guide](https://docs.docker.com/get-docker/))
- Basic understanding of Docker commands
- The project must have been run at least once to generate the model file

### Docker Deployment Steps

#### 1. Understanding the Docker Files
The notebook automatically generates two important files:
- `Dockerfile`: Defines how to build the Docker image
- `predict.py`: A Flask API that serves model predictions

#### 2. Building the Docker Image
From the project root directory, run:
```bash
# Build the image with a tag
docker build -t satisfaction-model:1.0.0 .
```

This command:
- Reads the Dockerfile in the current directory
- Creates an image named "satisfaction-model" with version "1.0.0"
- Installs all dependencies specified in requirements.txt
- Copies the model and prediction script into the image

#### 3. Verifying the Image Creation
Verify that your image was created successfully:
```bash
docker images
```

You should see "satisfaction-model" in the list of images.

#### 4. Running the Docker Container
Start a container from your image:
```bash
docker run -p 5000:5000 --name telecom-model satisfaction-model:1.0.0
```

This command:
- Creates and starts a container named "telecom-model"
- Maps port 5000 of the container to port 5000 on your host
- Uses the satisfaction-model:1.0.0 image
- Starts the Flask API service

#### 5. Making Predictions
With the container running, you can make predictions via HTTP requests:
```bash
# Using curl
curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{"engagement_score": 0.8, "experience_score": 0.7}'

# Or using Python
import requests
response = requests.post(
    "http://localhost:5000/predict",
    json={"engagement_score": 0.8, "experience_score": 0.7}
)
print(response.json())
```

#### 6. Managing the Docker Container
```bash
# List running containers
docker ps

# Stop the container
docker stop telecom-model

# Start an existing container
docker start telecom-model

# Remove a container (must be stopped first)
docker rm telecom-model
```

#### 7. Advanced Docker Options
- Run the container in detached mode (background):
  ```bash
  docker run -d -p 5000:5000 --name telecom-model satisfaction-model:1.0.0
  ```

- View container logs:
  ```bash
  docker logs telecom-model
  ```

- Access a shell inside the container:
  ```bash
  docker exec -it telecom-model bash
  ```

- Configure environment variables:
  ```bash
  docker run -p 5000:5000 -e DEBUG=True --name telecom-model satisfaction-model:1.0.0
  ```

#### 8. Troubleshooting Docker Deployment
- If the container exits immediately, check logs:
  ```bash
  docker logs telecom-model
  ```

- If you can't connect to the API, verify the port mapping:
  ```bash
  docker port telecom-model
  ```

- If the model file is missing, ensure you've run the notebook completely:
  ```bash
  # Check if models directory exists and contains the model file
  ls -la models/
  ```

- Update the Docker image after changes:
  ```bash
  docker build -t satisfaction-model:1.0.1 .
  ```

### CI/CD Integration for Model Deployment

The Docker containerization can be integrated into CI/CD (Continuous Integration/Continuous Deployment) pipelines to automate the model deployment process, ensuring consistent and reliable deployments with minimal manual intervention.

#### CI/CD Pipeline Overview

A complete CI/CD pipeline for this project might include the following stages:

1. **Code Changes & Version Control**
   - Push changes to a Git repository (GitHub, GitLab, Bitbucket)
   - Create feature branches for model improvements
   - Use pull requests for code review

2. **Continuous Integration**
   - Automated testing of the model code and API
   - Verification of model performance metrics
   - Validation of model inputs and outputs
   - Unit tests for the Flask API endpoints

3. **Model Training & Evaluation**
   - Scheduled or trigger-based model retraining
   - Automated MLflow tracking of model metrics
   - Model validation against performance thresholds
   - Comparison with previous model versions

4. **Docker Image Building**
   - Automated Docker image building on successful tests
   - Image versioning based on Git tags or commits
   - Multi-stage builds for optimized images
   - Security scanning of Docker images

5. **Artifact Storage**
   - Push Docker images to a container registry (Docker Hub, AWS ECR, Google GCR)
   - Store model artifacts in MLflow or dedicated storage
   - Version control for both code and model artifacts

6. **Deployment Automation**
   - Staging environment deployment for validation
   - Production deployment after approval
   - Deployment notifications and logging
   - Rollback capabilities for failed deployments

#### Example CI/CD Implementation with GitHub Actions

Here's an example GitHub Actions workflow file (`.github/workflows/model-deploy.yml`):

```yaml
name: Model CI/CD Pipeline

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    - name: Run tests
      run: |
        pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: success() && (github.event_name == 'push')
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run notebook to generate model
      run: |
        pip install jupyter nbconvert
        jupyter nbconvert --to python analysis.ipynb
        python analysis.py
        
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
      
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
        
    - name: Extract metadata for Docker
      id: meta
      uses: docker/metadata-action@v3
      with:
        images: yourusername/satisfaction-model
        tags: |
          type=semver,pattern={{version}}
          type=sha,format=short
          
    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
    - name: Deploy to production
      run: |
        # Deploy commands - examples might include:
        # - kubectl apply for Kubernetes
        # - AWS ECS deployment
        # - SSH into server and docker-compose up
        echo "Deploying version $(echo $GITHUB_REF | cut -d / -f 3)"
```

#### CI/CD with MLOps Platforms

For more advanced model lifecycle management, consider integrating with specialized MLOps platforms:

1. **MLflow + Kubernetes**
   - Use MLflow for model tracking and registry
   - Deploy models as Kubernetes services
   - Implement canary deployments for new models

2. **Kubeflow**
   - End-to-end ML platform on Kubernetes
   - Pipelines for model training, validation, and deployment
   - Automatic scaling of model serving

3. **Cloud-specific MLOps**
   - AWS SageMaker Pipelines
   - Google Cloud AI Platform
   - Azure ML Pipelines

#### Monitoring and Feedback Loop

Complete the CI/CD cycle with monitoring and feedback:

1. **Model Performance Monitoring**
   - Track prediction accuracy over time
   - Set up alerts for model drift
   - Log all predictions for auditing

2. **Automated Retraining Triggers**
   - Schedule periodic retraining
   - Trigger retraining when performance drops
   - A/B testing of model versions

3. **Feedback Integration**
   - Collect user feedback on predictions
   - Integrate feedback into training data
   - Document model improvements over time

By implementing a robust CI/CD pipeline, you ensure that your satisfaction prediction model remains accurate, up-to-date, and reliably deployed with minimal manual intervention.

## Key Findings and Recommendations

### User Overview Analysis (Task 1)
- Handset distribution reveals strategic market positioning opportunities, with top manufacturers dominating the user base
- Application usage is dominated by video and social media applications, indicating opportunities for specialized data plans
- Decile-based segmentation shows that the top 50% of users (by session duration) generate a disproportionate amount of data traffic, highlighting high-value customer segments
- Correlation analysis between applications shows meaningful relationships that can be leveraged for targeted marketing

### User Engagement Analysis (Task 2)
- Three distinct engagement clusters were identified through k-means clustering
- Top engagement metrics vary significantly across user segments, with the highest engaged users showing much higher activity than average
- Application-specific engagement reveals different user personas that can be targeted with specialized offerings
- Elbow method analysis suggests the optimal k value for engagement segmentation

### User Experience Analysis (Task 3)
- Key technical issues identified in network performance metrics, particularly for certain handset types
- Throughput and TCP retransmission rates vary significantly by device, indicating possible optimization needs
- Experience clustering revealed three distinct quality-of-service segments among the user base
- Specific handset types show concerning performance metrics that may require targeted technical improvements

### User Satisfaction Analysis (Task 4)
- Combined engagement and experience metrics provide holistic satisfaction scores
- Regression model successfully predicts customer satisfaction with good accuracy
- Satisfaction clusters reveal distinct customer segments with different retention risks
- Model deployment and tracking implementation enables ongoing satisfaction monitoring

### Acquisition Recommendation

**Recommendation: PROCEED with acquisition**

#### Positive Factors:
- Strong user base with clear high-value segments identified through decile analysis
- Identifiable technical issues that can be addressed through targeted infrastructure investment
- Predictable satisfaction drivers that enable proactive customer management
- Clear growth potential in specific application areas and user segments

#### Required Actions Post-Acquisition:
1. Address network performance issues for specific handset types
2. Develop specialized plans for users of top applications
3. Implement satisfaction monitoring system to track improvements
4. Focus retention efforts on high-value segments identified in decile analysis

#### Expected Returns:
- Improved retention in high-value segments
- Enhanced average revenue per user through targeted offerings
- Reduced network costs through optimized infrastructure investment
- Competitive differentiation through improved quality of service

### Analysis Limitations
- Limited time period of data collection; seasonality effects not captured
- Missing demographic information that could enhance targeting
- No competitive benchmark data for relative performance evaluation
- Satisfaction model requires ongoing validation with actual customer feedback
- MySQL database implementation needed for production-level deployment
- Limited visibility into device-specific technical issues beyond aggregate metrics

## License
This project is for educational purposes only. Data used is proprietary. 