# Todo Application using Python Flask on AWS EC2 with Docker (Automated Deployment)

This project demonstrates how to build a Todo application using Python Flask, containerize it with Docker, and automate the entire deployment process to an AWS EC2 instance using GitHub Actions. The process involves automatically building the Docker image, pushing it to DockerHub, creating an EC2 instance, and deploying the application.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Process Overview](#process-overview)
   - [1. Dockerizing the Application](#1-dockerizing-the-application)
   - [2. Automating Deployment with GitHub Actions](#2-automating-deployment-with-github-actions)
   - [3. Deploying to AWS EC2](#3-deploying-to-aws-ec2)
5. [Running Locally](#running-locally)
6. [Screenshots](#screenshots)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview

This project demonstrates how to:
- Build a **Todo application** using **Python Flask**.
- Dockerize the Flask app.
- Automate the entire deployment process using GitHub Actions, including:
  - Building the Docker image.
  - Pushing the Docker image to DockerHub.
  - Creating and configuring an AWS EC2 instance.
  - Pulling the Docker image from DockerHub and running the container.

## Technologies Used
- **Python** (Flask)
- **Docker** (for containerization)
- **AWS EC2** (for deployment)
- **GitHub Actions** (for CI/CD automation)
- **DockerHub** (for storing Docker images)

## Prerequisites

Before starting, ensure you have the following:
1. An AWS account with permissions to create EC2 instances.
2. A DockerHub account to push the Docker image.
3. A GitHub repository with access to GitHub Actions.

## Process Overview

### 1. Dockerizing the Application

The application is containerized using Docker to simplify deployment. The Docker image is built from the source code and pushed to DockerHub, where it can be pulled by the EC2 instance.

### 2. Automating Deployment with GitHub Actions

The deployment is fully automated through GitHub Actions, which:
- Builds the Docker image from the application code.
- Pushes the Docker image to DockerHub.
- Uses AWS CLI commands to:
  - Launch an EC2 instance.
  - Configure the instance's security groups.
  - SSH into the instance, pull the Docker image from DockerHub, and run the container.

### 3. Deploying to AWS EC2

The application is deployed on an AWS EC2 instance, which:
- Pulls the Docker image from DockerHub.
- Runs the Todo application in a Docker container on port 5000.
- Automatically configures the necessary networking and security settings to allow external access.

## Running Locally

You can also run the Todo application locally in Docker:
1. Build the Docker image locally.
2. Run the Docker container and access the Todo application from your browser.

## Screenshots

#### 1. Automated Deployment via GitHub Actions

![GitHub Actions Workflow](/images/Github%20Action%20Workflow.jpg)

#### 2. Application Running on EC2
![Todo App on EC2](/images/Task%20master-Homepage.jpg)


## Contributing

If you'd like to contribute to this project, feel free to submit issues or pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

