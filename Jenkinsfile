pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh """
                    python3 -m venv venv
                    python3 venv/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    python3 -m unittest discover tests
                """
            }
        }
        stage('Deploy') {
            steps {
                // SSH deploy to EC2
                sh 'scp -r * ec2-user@44.246.138.83:/home/ec2-user/app/'
                sh 'ssh ec2-user@44.246.138.83 "cd /home/ec2-user/app && nohup python3 app.py &"'
            }
        }
    }
}
