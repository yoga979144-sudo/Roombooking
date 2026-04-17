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
                // Use 'bat' instead of 'sh' for Windows
                bat 'pip install -r requirements.txt'
                bat 'pytest'
            }
        }

        stage('Build & Push Docker') {
            steps {
                script {
                    // This requires the Docker Pipeline plugin installed in Jenkins
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
                // Ensure the 'Kubernetes CLI' plugin is installed
                withKubeConfig([credentialsId: 'k8s-creds']) {
                    // Windows batch equivalent to update the image tag in the YAML
                    bat "powershell -Command \"(Get-Content k8s/deployment.yaml) -replace 'image:.*', 'image: ${DOCKER_IMAGE}:${DOCKER_TAG}' | Set-Content k8s/deployment.yaml\""
                    bat "kubectl apply -f k8s/deployment.yaml"
                    bat "kubectl apply -f k8s/service.yaml"
                }
            }
        }
    }
}
