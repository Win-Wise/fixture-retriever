# Create the function
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "functions/first-function/src/lambda.py"
  output_path = "functions/first-function/src/lambda.zip"
}

resource "aws_lambda_function" "test_lambda" {
  function_name    = "hello-world"
  role             = var.lambda_role.arn
  handler          = "lambda.lambda_handler"
  runtime          = "python3.11"
  filename         = "functions/first-function/src/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
}