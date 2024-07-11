# Create the function
data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "functions/fixture-populator/src"
  output_path = "functions/fixture-populator/lambda.zip"
}

resource "aws_lambda_function" "fixture_populator" {
  function_name    = "fixture-populator"
  role             = var.lambda_role.arn
  handler          = "lambda.lambda_handler"
  runtime          = "python3.11"
  filename         = "functions/fixture-populator/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  layers           = [var.lambda_layer.arn]
  timeout          = 900
  environment {
    variables = {
      MONGODB_URI = "mongodb+srv://tributary-dev.ygqeljj.mongodb.net/arbriver?authSource=$external&authMechanism=MONGODB-AWS"
      RAPIDAPI_KEY = var.rapidapi_api_key
      PYTHONHASHSEED = 143
    }
  }
}