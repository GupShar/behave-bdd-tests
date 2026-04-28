pipeline {

    agent any

    triggers {
        githubPush()
        cron('0 0 * * *')
    }

    environment {
        // Run "which python3" in your Mac Terminal to confirm your path
        // Apple Silicon (M1/M2/M3): /opt/homebrew/bin/python3
        // Intel Mac: /usr/local/bin/python3
        PYTHON      = '/opt/homebrew/bin/python3'
        VENV_DIR    = 'venv'
        REPORTS_DIR = 'reports'
        CI          = 'true'
    }

    stages {

        stage('Build Info') {
            steps {
                echo "Job       : ${env.JOB_NAME}"
                echo "Build No  : ${env.BUILD_NUMBER}"
                echo "Branch    : ${env.GIT_BRANCH}"
                echo "Python    : ${env.PYTHON}"
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
                echo "Code checked out from GitHub"
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    echo "Python version:"
                    ${PYTHON} --version

                    echo "Creating virtual environment..."
                    ${PYTHON} -m venv ${VENV_DIR}

                    echo "Installing dependencies..."
                    ${VENV_DIR}/bin/pip install --upgrade pip --quiet
                    ${VENV_DIR}/bin/pip install -r requirements.txt --quiet

                    echo "Installed packages:"
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
                    echo "Some tests failed - marking build UNSTABLE"
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
                echo "HTML report published - check left sidebar"
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
            echo "UNSTABLE - some tests failed. Check the Behave Test Report."
        }
        failure {
            echo "Pipeline FAILED - check Python path, Chrome, GitHub access."
        }
    }
}
