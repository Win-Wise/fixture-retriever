# Create the function
data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "functions/first-function/src"
  output_path = "functions/first-function/lambda.zip"
}

resource "aws_lambda_function" "event_scraper" {
  function_name    = "event-scraper"
  role             = var.lambda_role.arn
  handler          = "lambda.lambda_handler"
  runtime          = "python3.11"
  filename         = "functions/first-function/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  layers           = [var.lambda_layer.arn]
  timeout          = 450
  environment {
    variables = {
      MONGODB_URI = "mongodb+srv://tributary-dev.ygqeljj.mongodb.net/arbriver?authSource=$external&authMechanism=MONGODB-AWS"
      CAESARS_EVENTS_REQUEST= "https://api.americanwagering.com/regions/us/locations/il/brands/czr/sb/v3/sports/{sport}/events/schedule"
      DRAFTKINGS_EVENTS_REQUEST= "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/{group}?format=json"
      DRAFTKINGS_GROUPS_REQUEST= "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v2/displaygroupinfo?format=json"
      ZR_API_KEY = var.zenrows_api_key
    }
  }
}