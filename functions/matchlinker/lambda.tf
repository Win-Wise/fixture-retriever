# Create the function
data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "functions/matchlinker/src"
  output_path = "functions/matchlinker/lambda.zip"
}

resource "aws_lambda_function" "match_linker" {
  function_name    = "match-linker"
  role             = var.lambda_role.arn
  handler          = "lambda.lambda_handler"
  runtime          = "python3.11"
  filename         = "functions/matchlinker/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  layers           = [var.lambda_layer.arn]
  timeout          = 900
  environment {
    variables = {
      MONGODB_URI = "mongodb+srv://tributary-dev.ygqeljj.mongodb.net/arbriver?authSource=$external&authMechanism=MONGODB-AWS"
      RAPIDAPI_API_KEY_SECRET = var.rapidapi_api_key_secret.arn
      PYTHONHASHSEED = 143
    }
  }
}