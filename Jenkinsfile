pipeline {

    agent any

    parameters {
        string(name: 'TICKERS', defaultValue: 'AAPL,GOOG,MSFT,NVDA', description: 'Comma-separated ticker symbols')
        string(name: 'THRESHOLD', defaultValue: '200', description: 'Alert threshold for price')
    }

    environment {
        SLACK_WEBHOOK = credentials('b010e98e-3667-4fc9-b7e2-5075fce052f8')
    }

    stages {
        stage("Approval") {
            steps {
                script {
                    input message: "Proceed to check stock prices for: ${params.TICKERS}?"
                }
            }
        }
        stage("Setup") {
            steps {
                script {
                    sh """
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage("Run Stock Price Alert") {
            steps {
                script {
                    withEnv([
                        "TICKERS=${params.TICKERS}",
                        "THRESHOLD=${params.THRESHOLD}",
                        "SLACK_WEBHOOK=${SLACK_WEBHOOK}"
                    ]) {
                        sh """
                            . venv/bin/activate
                            python3 app.py
                        """
                    }
                }
            }
        }
        stage("Archive Logs") {
            steps {
                script {
                    archiveArtifacts artifacts: 'stock_log.csv', fingerprint: true
                }
            }
        }
    }
}