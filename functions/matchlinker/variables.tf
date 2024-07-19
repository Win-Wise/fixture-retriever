variable "lambda_role" {
  type = any
  description = "the lambda execution role"
}

variable "lambda_layer" {
  type = any
  description = "the lambda layer used"
}

variable "rapidapi_api_key_secret" {
  type = any
  description = "the api key for using the rapidapi service"
}