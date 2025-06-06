pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        SLACK_CHANNEL = "ai-results"
    }

    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt && python -m playwright install'
            }
        }

        stage('Run Test') {
            steps {
                sh 'source venv/bin/activate && python slack_simulator.py'
                sh 'source venv/bin/activate && robot -d reports tests/test_browser_use.robot'
            }
        }

        stage('Send to Slack') {
            steps {
                sh 'source venv/bin/activate && python slack_reporter.py'
            }
        }
    }

    post {
        failure {
            echo 'Test failed ❌'
        }
    }
}
