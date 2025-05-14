pipeline {

    agent any

    environment {
        SLACK_WEBHOOK = credentials('b010e98e-3667-4fc9-b7e2-5075fce052f8')
        TICKER = "AAPL"
        THRESHOLD = 1000
    }

    stages {
        stage("Approval") {
            steps {
                script {
                    input message: "Proceed to check stock prices for: ${TICKER}?"
                }
            }
        }
        stage("Setup") {
            steps {
                script {
                    sh """
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage("Run Stock Price Alert") {
            steps {
                script {
                    withEnv([
                        "TICKER=${TICKER}"
                        "THRESHOLD=${THRESHOLD}"
                        "SLACK_WEBHOOK=${SLACK_WEBHOOK}"
                    ]) {
                        sh """
                            source venv/bin/activate
                            python3 app.py
                        """
                    }
                }
            }
        }
    }
}