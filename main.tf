terraform {
  cloud {
    organization = "arbriver"

    workspaces {
      name = "fixture-retriever"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.55.0"
    }
  }
  required_version = ">= 1.1.0"
}

provider "aws" {
  region = "us-east-1"
}

data "terraform_remote_state" "base_workspace" {
  backend = "remote"

  config = {
    organization = "arbriver"

    workspaces = {
      name = "arbriver-infra-base"
    }
  }
}

module "match-linker" {
  source = "./functions/matchlinker"
  lambda_role = data.terraform_remote_state.base_workspace.outputs.lambda_execution_role
  lambda_layer = data.terraform_remote_state.base_workspace.outputs.lambda_base_layer
  rapidapi_api_key_secret = data.terraform_remote_state.base_workspace.outputs.rapidapi_api_key_secret
}

module "event-scraper" {
  source = "./functions/eventscraper"
  lambda_role = data.terraform_remote_state.base_workspace.outputs.lambda_execution_role
  lambda_layer = data.terraform_remote_state.base_workspace.outputs.lambda_base_layer
  zenrows_api_key_secret = data.terraform_remote_state.base_workspace.outputs.zenrows_api_key_secret
  betfair_app_key_secret = data.terraform_remote_state.base_workspace.outputs.betfair_app_key_secret
  betfair_password_secret = data.terraform_remote_state.base_workspace.outputs.betfair_password_secret
  uk_https_proxy_secret = data.terraform_remote_state.base_workspace.outputs.uk_https_proxy_secret
  betfair_username = var.betfair_username
}

module "statemachine"{
  source = "./statemachine"
  statemachine_role = data.terraform_remote_state.base_workspace.outputs.statemachine_execution_role
  processing_lambda = module.event-scraper.lambda
  populator_lambda = module.match-linker.lambda
}