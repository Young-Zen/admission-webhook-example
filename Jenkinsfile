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
          sh 'echo "${tencent_serverless}" > .tmp'
          sh '''
            SecretId=$(cat .tmp | jq -r .SecretId)
            SecretKey=$(cat .tmp | jq -r .SecretKey)
            token=$(cat .tmp | jq -r .token)
            AppId=$(cat .tmp | jq -r .AppId)
            echo "TENCENT_SECRET_ID=${SecretId}" >> ./serverless/.env
            echo "TENCENT_SECRET_KEY=${SecretKey}" >> ./serverless/.env
            echo "TENCENT_APP_ID=${AppId}" >> ./serverless/.env
            echo "TENCENT_TOKEN=${token}" >> ./serverless/.env
             '''
          sh 'cp .env ./serverless'
          sh 'cd serverless && cat .env'
          sh 'cd serverless && npm run bootstrap && sls deploy --all | tee log.log'
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