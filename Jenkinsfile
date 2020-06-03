pipeline {
  agent any
  stages {
    stage("检出") {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: env.GIT_BUILD_REF]],
          userRemoteConfigs: [[
            url: env.GIT_REPO_URL,
            credentialsId: env.CREDENTIALS_ID
        ]]])
      }
    }
    stage('升级 Serverless SDK') {
      steps {
        sh 'npm update -g serverless'
      }
    }
    stage('部署 Serverless 服务') {
      steps {
        withCredentials([string(credentialsId:"3bbd3a13-48fc-499d-8d2d-c51a098ec9bc", variable:'tencent_serverless')]) {
          sh 'echo "${tencent_serverless}" > .env_temp'
          sh 'echo "${tencent_serverless}" | base64'
          sh 'cd serverless && npm run bootstrap && sls deploy --all | tee log.log'
          sh 'rm .env_temp'
        }
        echo '部署完成'
      }
    }
    stage('输出 Endpoint') {
      steps {
        sh 'cd serverless && cat log.log | grep apigw.tencentcs.com'
      }
    }
  }
}