pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/annadichandana/hostel-room-allotment.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python manage.py test
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Deploy with Waitress') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                waitress-serve --listen=0.0.0.0:8000 hostel_allocation.wsgi:application
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed. Check logs.'
        }
    }
}
