'use strict'

const path = require('path')
const util = require('util')
const exec = util.promisify(require('child_process').exec)

const rootDir = path.join(__dirname, '..')
const apiDir = path.join(rootDir, 'api')

async function installDependencies(dir) {
  await exec('npm install', {
    cwd: dir
  })
}

/* eslint-disable no-console*/
async function bootstrap() {
  console.log('Start install dependencies...\n')
  console.log('Start install api dependencies...\n')
  await installDependencies(apiDir)
  console.log('Api dependencies installed success.')
}

bootstrap()

process.on('unhandledRejection', (e) => {
  throw e
})