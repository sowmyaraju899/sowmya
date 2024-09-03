pipeline {
    agent any 
    environment {
    DOCKERHUB_CREDENTIALS = credentials('12daa05c-c4a1-4d1c-8f40-e4c72b158eb8')
    }
    stages { 
        stage('SCM Checkout') {
            steps{
                git branch: 'main', url:'https://github.com/sowmyaraju899/sowmya.git'
            }
        }

        stage('Build docker image') {
            steps {  
                sh 'docker-compose build' 
            }
        }
        stage('login to dockerhub') {
            steps{
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Push docker image') {
            steps {
                sh 'docker-compose push'
            }
        }
               }
}
