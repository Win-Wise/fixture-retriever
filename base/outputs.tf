output "lambda_execution_role"{
  value = aws_iam_role.function_role
}

output "lambda_layer" {
  value = aws_lambda_layer_version.lambda_layer
}