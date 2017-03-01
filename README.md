# eb_deployer Resource

[![Build Status](https://travis-ci.org/cosee-concourse/eb_deployer-resource.svg?branch=master)](https://travis-ci.org/cosee-concourse/eb_deployer-resource) [![Docker Repository on Quay](https://quay.io/repository/cosee-concourse/eb_deployer-resource/status "Docker Repository on Quay")](https://quay.io/repository/cosee-concourse/eb_deployer-resource)


Deploys applications to Elastic Beanstalk.
For smoke tests curl can be used. For other tools you need to add the alpine package to 
the Dockerfile of this resource.

## Source Configuration

* `access_key_id`: *Required.* The AWS access key.

* `secret_access_key`: *Required.* The AWS secret key.

## Behavior

### `check`: Checks configuration

Checks for correct source configuration.

### `in`: Saves environment as file

* Saves a file with the name `env` in the directory containing the name of the deployed environment. 
Calling `in` before calling `out` in the same pipeline can cause unexpected behavior.

#### Parameters

*None.*

### `out`: Deploys or removes Elastic Beanstalk application.

Uses eb_deployer configuration from `config_file` and `artifact_file` to deploy/remove application.

#### Parameters
 
* `config_file`: *Required* Folder path that contains eb_deployer.yml. 

* `artifact_file`: Path to artifact file (full path) used as package for deployment. 
 
* `env_file`: Path to a file that contains the name of the environment to deploy/remove

* `env`: Environment to deploy/remove

* `deploy`: If set to `true` deploys the application.

* `remove`: If set to `true` removes the application.

Either `env_file` or `env` has to be set.
If neither is set it defaults to "dev"
Also either `deploy` or `remove` has to be set to true.


## Example Configuration

### Resource Type
``` yaml
- name: ebdeployer
  type: docker-image
  source:
    repository: quay.io/cosee-concourse/eb_deployer-resource
```
### Resource

``` yaml
- name: deploy
  type: ebdeployer
  source:
    access_key_id: ACCESS-KEY
    secret_access_key: SECRET
```

### Plan

``` yaml
- get: deploy
```

#### Deploy with fixed environment name

``` yaml
- put: deploy
  params:
    deploy: true
    env: dev
    artifact_file: artifacts/package.zip
    config_file: source/ci
```

#### Deploy with environment name from file

``` yaml
- put: deploy
  params:
    deploy: true
    env_file: naming/env
    artifact_file: artifacts/package.zip
    config_file: source/ci
```
#### Remove with fixed environment name

``` yaml
- put: deploy
  params:
    remove: true
    env: dev
    config_file: source/ci
```

#### Remove with environment name from file

``` yaml
- put: deploy
  params:
    remove: true
    env_file: naming/env
    config_file: source/ci
```
