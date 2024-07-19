variable "lambda_role" {
  type = any
  description = "the lambda execution role"
}

variable "lambda_layer" {
  type = any
  description = "the lambda layer used"
}

variable "zenrows_api_key_secret" {
  type = any
  description = "the api key for using the zenrows proxy"
}

variable "betfair_app_key_secret" {
  type = any
  description = "the api key for using the betfair service"
}

variable "betfair_password_secret" {
  type = any
  description = "the password for using the betfair service"
}

variable "uk_https_proxy_secret" {
  type = any
  description = "the proxy secret for using the betfair service"
}

