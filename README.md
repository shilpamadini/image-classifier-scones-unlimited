# Scones Unlimited – Image Classifier Project
## Overview

This project demonstrates the end-to-end process of building, training, deploying, and orchestrating an image classification model using AWS SageMaker, Lambda, and Step Functions.

The model classifies delivery vehicles for Scones Unlimited, a logistics company, into bicycles and motorcycles to optimize delivery routing and logistics operations.

# Project Goals

Build a scalable image classification pipeline using AWS SageMaker.

Train a CNN model using the CIFAR-100 dataset to distinguish bicycles and motorcycles.

Deploy the trained model as a real-time inference endpoint.

Enable data capture and model monitoring.

Build a Step Function workflow with Lambda functions to:

Fetch and serialize image data from S3.

Invoke the deployed SageMaker endpoint.

Filter predictions based on a confidence threshold.

# Steps Implemented
## Data Staging

Used the CIFAR-100 dataset (Python version).

Extracted, transformed, and filtered only the bicycle and motorcycle images.

Saved the images as .png files in local train/ and test/ folders.

Uploaded data and manifest files (train.lst, test.lst) to an S3 bucket.

# Model Training & Deployment

Retrieved the prebuilt SageMaker image-classification container.

Trained the model using SageMaker’s built-in algorithm on an ml.p3.2xlarge instance.

Achieved ~81% validation accuracy.

Deployed the model on a ml.m5.xlarge endpoint.

Configured data capture for model monitoring.

# Lambda Functions

Three Lambda functions were built to support the Step Function workflow:

serializeImageData – Downloads and base64-encodes an image from S3.

classifyImageData – Invokes the SageMaker endpoint and returns prediction probabilities.

filterInferences – Checks if the model confidence exceeds the defined threshold (e.g., 0.94).

# Step Function Workflow

Orchestrated the above three Lambdas in sequence:

Serialize → Classify → Filter

Configured transitions between steps and ensured outputs were properly mapped.

Tested with multiple executions to validate successful and failure paths.

# Model Monitoring

Verified data captured in S3 under /data_capture/AllTraffic/...

Visualized recent inference confidence trends over time using matplotlib.

# Evaluation

Sampled 50 training images and ran inference against the deployed endpoint.

Compared predictions with true labels.

Built a scatter plot visualization of prediction confidence vs. true labels:

Blue dots = bicycles

Red dots = motorcycles

Green dashed line = confidence threshold (0.94)

# Results

Validation Accuracy: ~81.7%

Sample Evaluation Accuracy (50 images): ~85–90%

Model confidence consistent across both classes (no major bias).


