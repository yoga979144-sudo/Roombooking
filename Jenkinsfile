pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "23mis0383/booking-app"
        DOCKER_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yoga979144-sudo/Roombooking.git'
            }
        }

        stage('Unit Tests') {
            steps {
                // Installs requirements and runs pytest
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }

        stage('Build & Push Docker') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        def appImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        appImage.push()
                        appImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'k8s-creds']) {
                    sh "sed -i 's|image:.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|' k8s/deployment.yaml"
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl apply -f k8s/service.yaml"
                }
            }
        }
    }
}