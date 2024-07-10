variable "lambda_role" {
  type = any
  description = "the lambda execution role"
}

variable "lambda_layer" {
  type = any
  description = "the lambda layer used"
}

variable "rapidapi_api_key" {
  type = string
  description = "the api key for using the rapidapi service"
}