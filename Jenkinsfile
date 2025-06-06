// pipeline {
//     agent any

//     environment {
//         SLACK_BOT_TOKEN = credentials('slack-token')
//         SLACK_CHANNEL = '#ai-results'
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 git branch: 'main',
//                     url: 'https://github.com/Rajanavee/ai-ui-test-browseruse.git'
//             }
//         }

//         stage('Setup Python & Dependencies') {
//             steps {
//                 sh '''
//                     python3 -m venv venv
//                     source venv/bin/activate
//                     pip install --upgrade pip
//                     pip install -r requirements.txt
//                     python -m playwright install
//                 '''
//             }
//         }

//         stage('Run Test') {
//             steps {
//                 sh '''
//                     source venv/bin/activate
//                     python slack_simulator.py
//                 '''
//             }
//         }
//     }

//     post {
//         always {
//             echo "📣 Sending final Slack message..."
//             sh '''
//                 source venv/bin/activate
//                 python slack_simulator.py
//             '''
//         }
//     }
// }

// pipeline {
//   agent any

//   environment {
//     SLACK_BOT_TOKEN = credentials('slack-token')  // Jenkins Credential ID
//     SLACK_CHANNEL = '#ai-results'
//   }

//   stages {
//     stage('Checkout') {
//       steps {
//         git url: 'https://github.com/Rajanavee/ai-ui-test-browseruse.git', branch: 'main'
//       }
//     }

//     stage('Setup Python & Dependencies') {
//       steps {
//         sh '''
//           python3 -m venv venv
//           source venv/bin/activate
//           pip install --upgrade pip
//           pip install -r requirements.txt
//           python -m playwright install
//         '''
//       }
//     }

//     stage('Run Test') {
//       steps {
//         sh '''
//           source venv/bin/activate
//           python slack_simulator.py
//         '''
//       }
//     }
//   }

//   post {
//     always {
//       echo '📣 Sending final Slack message...'
//       sh '''
//         source venv/bin/activate
//         python slack_simulator.py
//       '''
//     }
//   }
// }



pipeline {
  agent any

  environment {
    SLACK_BOT_TOKEN = credentials('slack-token')  // your Jenkins secret ID
    SLACK_CHANNEL = '#ai-results'
  }

  stages {
    stage('Send Simple Slack Message') {
      steps {
        sh '''
          python3 -m venv venv
          source venv/bin/activate
          pip install -U pip python-dotenv requests
          python slack_ping.py
        '''
      }
    }
  }
}
