pipeline {

    agent any

    triggers {
        githubPush()
        cron('0 0 * * *')
    }

    environment {
        PYTHON      = '/opt/homebrew/bin/python3'
        VENV_DIR    = 'venv'
        REPORTS_DIR = 'reports'
        CI          = 'true'
    }

    stages {

        stage('Build Info') {
            steps {
                echo "Job    : ${env.JOB_NAME}"
                echo "Build  : ${env.BUILD_NUMBER}"
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
                echo "Code checked out"
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    ${PYTHON} --version
                    ${PYTHON} -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip --quiet
                    ${VENV_DIR}/bin/pip install -r requirements.txt --quiet
                    ${VENV_DIR}/bin/pip list
                '''
            }
        }

        stage('Run BDD Tests') {
            steps {
                sh '''
                    mkdir -p ${REPORTS_DIR}
                    ${VENV_DIR}/bin/behave \
                        --no-capture \
                        --format pretty \
                        --format json --outfile ${REPORTS_DIR}/behave-report.json \
                        --format html --outfile ${REPORTS_DIR}/behave-report.html \
                        features/
                '''
            }
            post {
                failure {
                    unstable('Test failures detected')
                }
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    allowMissing         : false,
                    alwaysLinkToLastBuild: true,
                    keepAll              : true,
                    reportDir            : "${REPORTS_DIR}",
                    reportFiles          : 'behave-report.html',
                    reportName           : 'Behave Test Report',
                    reportTitles         : 'BDD Test Results'
                ])
                echo "Report published"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }
        success {
            echo "All tests passed!"
        }
        unstable {
            echo "Some tests failed. Check the Behave Test Report."
        }
        failure {
            echo "Pipeline FAILED. Check Python path and Chrome."
        }
    }
}
