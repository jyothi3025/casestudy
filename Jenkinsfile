pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'  // set in Jenkins credentials
    DOCKER_IMAGE = "yourdockerhubusername/calorie-app"
    KUBECONFIG_CREDENTIAL = 'kubeconfig-credentials-id' // optional: Kubeconfig stored as secret
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/yourusername/your-repo.git', branch: 'main'
      }
    }

    stage('Build Image') {
      steps {
        script {
          docker.build("${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}")
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh """
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            docker tag ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER} ${env.DOCKER_IMAGE}:latest
            docker push ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}
            docker push ${env.DOCKER_IMAGE}:latest
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        // Option A: If kubectl is configured on Jenkins agent and cluster access exists
        // Update image in k8s manifest and apply
        sh """
          sed -i 's|image:.*|image: ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}|' k8s/deployment.yaml
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
        """
        // Option B: If using kubeconfig credential, you could write it to file before running kubectl
      }
    }
  }

  post {
    success {
      echo "Pipeline completed successfully."
    }
    failure {
      echo "Pipeline failed."
    }
  }
}
