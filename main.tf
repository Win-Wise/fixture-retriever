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

module "base"{
  source = "./base"
}

module "fixture-populator" {
  source = "./functions/fixture-populator"
  lambda_role = module.base.lambda_execution_role
  lambda_layer = module.base.lambda_layer
  rapidapi_api_key = var.rapidapi_api_key
}

module "first-function" {
  source = "./functions/first-function"
  lambda_role = module.base.lambda_execution_role
  lambda_layer = module.base.lambda_layer
  zenrows_api_key = var.zenrows_api_key
}

module "statemachine"{
  source = "./statemachine"
  processing_lambda = module.first-function
}