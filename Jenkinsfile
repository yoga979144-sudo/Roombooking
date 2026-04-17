pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "23mis0383/booking-app"
        DOCKER_TAG = "${env.BUILD_ID}"
    }

    stages {
        // We removed the manual 'Checkout' stage because Jenkins does it automatically 
        // via the 'Declarative: Checkout SCM' step you see in your logs.

        stage('Unit Tests') {
            steps {
                bat 'python -m pip install --upgrade flask werkzeug flask-sqlalchemy pytest'
                bat 'python -m pytest'
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
                    bat "powershell -Command \"(Get-Content k8s/deployment.yaml) -replace 'image:.*', 'image: ${DOCKER_IMAGE}:${DOCKER_TAG}' | Set-Content k8s/deployment.yaml\""
                    bat "kubectl apply -f k8s/deployment.yaml"
                    bat "kubectl apply -f k8s/service.yaml"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}

