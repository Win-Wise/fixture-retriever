# Explicitly create the function’s log group to set retention and allow auto-cleanup
resource "aws_cloudwatch_log_group" "lambda_function_log" {
  retention_in_days = 7
  name              = "/aws/lambda/${aws_lambda_function.fixture_populator.function_name}"
  lifecycle {
    prevent_destroy = false
  }
}