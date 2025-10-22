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
                "C:\\Users\\annad\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv venv
                call venv\\Scripts\\activate
                python -m pip install --upgrade pip
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
                waitress-serve --listen=0.0.0.0:8000 hostel.wsgi:application
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment failed. Check logs."
        }
    }
}
