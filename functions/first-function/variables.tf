variable "lambda_role" {
  type = any
  description = "the lambda execution role"
}

variable "lambda_layer" {
  type = any
  description = "the lambda layer used"
}

variable "zenrows_api_key" {
  type = any
  description = "the api key for using the zenrows proxy"
}