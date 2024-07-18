output "lambda_layer" {
  value = module.base.lambda_layer
}

output "lambda_execution_role" {
  value = module.base.lambda_execution_role
}

output "arbriver_bucket" {
  value = aws_s3_bucket.arbriver_bucket
}

output "betfair_password_secret" {
  value = aws_secretsmanager_secret.betfair_password
}

output "betfair_app_key_secret" {
  value = aws_secretsmanager_secret.betfair_app_key
}