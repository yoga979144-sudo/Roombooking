pipeline {
    agent any

    environment {
        // Change this to your actual Docker Hub username
        DOCKER_IMAGE = "23mis0383/booking-app"
        DOCKER_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clones your code from GitHub
                git branch: 'main', url: 'https://github.com'
            }
        }

        stage('Unit Tests') {
            steps {
                // Fixes the Werkzeug/Flask version mismatch and runs tests
                bat 'python -m pip install --upgrade flask werkzeug flask-sqlalchemy pytest'
                bat 'python -m pytest'
            }
        }

        stage('Build & Push Docker') {
            steps {
                script {
                    // Requires 'Docker Pipeline' plugin and 'dockerhub-creds' in Jenkins
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
                // Requires 'Kubernetes CLI' plugin and 'k8s-creds' in Jenkins
                withKubeConfig([credentialsId: 'k8s-creds']) {
                    // Updates the image tag in deployment.yaml using PowerShell
                    bat "powershell -Command \"(Get-Content k8s/deployment.yaml) -replace 'image:.*', 'image: ${DOCKER_IMAGE}:${DOCKER_TAG}' | Set-Content k8s/deployment.yaml\""
                    
                    // Applies changes to the cluster
                    bat "kubectl apply -f k8s/deployment.yaml"
                    bat "kubectl apply -f k8s/service.yaml"
                }
            }
        }
    }

    post {
        always {
            // Cleans up the workspace after the build finishes
            cleanWs()
        }
    }
}

