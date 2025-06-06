pipeline {
    agent any

    environment {
        SLACK_BOT_TOKEN = credentials('slack-token') // From Jenkins Credentials > Secret Text
        SLACK_CHANNEL = "ai-results"
        PYTHONIOENCODING = "utf-8"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Rajanavee/ai-ui-test-browseruse.git'
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m playwright install
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                    source venv/bin/activate
                    python slack_simulator.py
                '''
            }
        }

        stage('Send to Slack') {
            when {
                expression { fileExists('screenshots/combined.png') }
            }
            steps {
                sh '''
                    curl -F file=@screenshots/combined.png \
                         -F "initial_comment=✅ AI UI Test Completed" \
                         -F channels=$SLACK_CHANNEL \
                         -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
                         https://slack.com/api/files.upload
                '''
            }
        }
    }

    post {
        success {
            echo "Test completed ✅"
        }
        failure {
            echo "Test failed ❌"
        }
    }
}
