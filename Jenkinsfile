// Jenkinsfile
// Behave + Selenium BDD Pipeline
// Triggers: GitHub webhook (every commit) + daily schedule
// Reports:  HTML report published in Jenkins UI

pipeline {

    agent any

    // ── Triggers ──────────────────────────────────────────────────────────
    triggers {
        githubPush()           // fires on every GitHub push/commit
        cron('0 0 * * *')      // fires every night at midnight
        // cron('0 8 * * 1-5') // alternative: weekdays at 8 AM
    }

    // ── Environment variables ──────────────────────────────────────────────
    environment {
        // ✅ Full path to python3 — Jenkins Tools has no Python option, so we use full path
        // Run `which python3` in your Mac Terminal to confirm which one to use:
        // Apple Silicon (M1/M2/M3) Mac → /opt/homebrew/bin/python3
        // Intel Mac                    → /usr/local/bin/python3
        PYTHON      = '/opt/homebrew/bin/python3'
        VENV_DIR    = 'venv'
        REPORTS_DIR = 'reports'
        CI          = 'true'   // tells environment.py to run Chrome headless
    }

    stages {

        // 1. Print build info
        stage('Build Info') {
            steps {
                echo "============================================"
                echo "Job       : ${env.JOB_NAME}"
                echo "Build #   : ${env.BUILD_NUMBER}"
                echo "Branch    : ${env.GIT_BRANCH}"
                echo "Triggered : ${currentBuild.getBuildCauses()[0].shortDescription}"
                echo "Python    : ${env.PYTHON}"
                echo "============================================"
            }
        }

        // 2. Checkout from GitHub
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Code checked out"
            }
        }

        // 3. Set up Python venv + install dependencies
        stage('Setup Environment') {
            steps {
                sh '''
                    echo "-- Python version --"
                    ${PYTHON} --version

                    echo "-- Creating virtual environment --"
                    ${PYTHON} -m venv ${VENV_DIR}

                    echo "-- Installing dependencies --"
                    ${VENV_DIR}/bin/pip install --upgrade pip --quiet
                    ${VENV_DIR}/bin/pip install -r requirements.txt --quiet

                    echo "-- Installed packages --"
                    ${VENV_DIR}/bin/pip list
                '''
            }
        }

        // 4. Run Behave BDD tests (headless Chrome via CI=true)
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
                    echo "❌ Tests failed — marking UNSTABLE so report still publishes"
                    unstable('Test failures detected')
                }
            }
        }

        // 5. Publish HTML report in Jenkins sidebar
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
                echo "✅ Report published — see left sidebar"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }
        success {
            echo "✅ All tests passed!"
        }
        unstable {
            echo "⚠️ UNSTABLE — some tests failed. Check the Behave Test Report."
        }
        failure {
            echo "❌ Pipeline FAILED — check Python path, Chrome, GitHub access."
        }
    }
}
