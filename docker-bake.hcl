group "default" {
  targets = ["backend", "model-server", "web"]
}

variable "BACKEND_REPOSITORY" {
  default = "insight/backend"
}

variable "WEB_SERVER_REPOSITORY" {
  default = "insight/web-server"
}

variable "MODEL_SERVER_REPOSITORY" {
  default = "insight/model-server"
}

variable "INTEGRATION_REPOSITORY" {
  default = "insight/integration"
}

variable "CLI_REPOSITORY" {
  default = "insight/cli"
}

variable "DEVCONTAINER_REPOSITORY" {
  default = "insight/devcontainer"
}

variable "TAG" {
  default = "latest"
}

target "backend" {
  context    = "backend"
  dockerfile = "Dockerfile"

  cache-to   = ["type=inline"]

  tags      = ["${BACKEND_REPOSITORY}:${TAG}"]
}

target "web" {
  context    = "web"
  dockerfile = "Dockerfile"

  cache-to   = ["type=inline"]

  tags      = ["${WEB_SERVER_REPOSITORY}:${TAG}"]
}

target "model-server" {
  context = "backend"

  dockerfile = "Dockerfile.model_server"

  cache-to   = ["type=inline"]

  tags      = ["${MODEL_SERVER_REPOSITORY}:${TAG}"]
}

target "integration" {
  context    = "backend"
  dockerfile = "tests/integration/Dockerfile"

  // Provide the base image via build context from the backend target
  contexts = {
    base = "target:backend"
  }

  tags      = ["${INTEGRATION_REPOSITORY}:${TAG}"]
}

target "cli" {
  context    = "cli"
  dockerfile = "Dockerfile"

  cache-to   = ["type=inline"]

  tags      = ["${CLI_REPOSITORY}:${TAG}"]
}

target "devcontainer" {
  context    = ".devcontainer"
  dockerfile = "Dockerfile"

  cache-to   = ["type=inline"]

  tags      = ["${DEVCONTAINER_REPOSITORY}:${TAG}"]
}
