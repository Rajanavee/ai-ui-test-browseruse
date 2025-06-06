pipeline {
  agent any

  environment {
    SLACK_BOT_TOKEN = credentials('slack-token')   // From Jenkins Credentials
    SLACK_CHANNEL = 'ai-results'
  }

  stages {
    stage('Clone Repo') {
      steps {
        git branch: 'main', url: 'https://github.com/Rajanavee/ai-ui-test-browseruse.git'
      }
    }

    stage('Setup Python & Install Deps') {
      steps {
        sh '''
          python3 -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install Pillow
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
        expression { currentBuild.currentResult == 'SUCCESS' }
      }
      steps {
        sh '''
          curl -F file=@screenshots/combined.png \
               -F "initial_comment=✅ AI Test Summary: Job #${BUILD_NUMBER} - *PASSED*" \
               -F channels=${SLACK_CHANNEL} \
               -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
               https://slack.com/api/files.upload
        '''
      }
    }
  }

  post {
    failure {
      echo 'Test failed ❌'
      sh '''
        curl -F file=@screenshots/combined.png \
             -F "initial_comment=❌ AI Test Summary: Job #${BUILD_NUMBER} - *FAILED*" \
             -F channels=${SLACK_CHANNEL} \
             -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
             https://slack.com/api/files.upload || true
      '''
    }
  }
}
