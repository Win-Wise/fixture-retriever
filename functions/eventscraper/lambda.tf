# Create the function
data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "functions/eventscraper/src"
  output_path = "functions/eventscraper/lambda.zip"
}

resource "aws_lambda_function" "event_scraper" {
  function_name    = "event-scraper"
  role             = var.lambda_role.arn
  handler          = "lambda.lambda_handler"
  runtime          = "python3.11"
  filename         = "functions/eventscraper/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  layers           = [var.lambda_layer.arn]
  timeout          = 450
  environment {
    variables = {
      MONGODB_URI = "mongodb+srv://tributary-dev.ygqeljj.mongodb.net/arbriver?authSource=$external&authMechanism=MONGODB-AWS"
      FANDUEL_EVENTS_REQUEST = "https://sbapi.il.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId={sport}&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FChicago"
      CAESARS_EVENTS_REQUEST= "https://api.americanwagering.com/regions/us/locations/il/brands/czr/sb/v3/sports/{sport}/events/schedule"
      BETRIVERS_EVENTS_REQUEST= "https://il.betrivers.com/api/service/sportsbook/offering/listview/events?cageCode=847&type=prematch&groupId={group}&pageNr={page}&pageSize=20&offset=0"
      DRAFTKINGS_EVENTS_REQUEST= "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/{group}?format=json"
      DRAFTKINGS_GROUPS_REQUEST= "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v2/displaygroupinfo?format=json"
      ZR_API_KEY_SECRET = var.zenrows_api_key_secret.arn
      BETFAIR_PASSWORD_SECRET = var.betfair_password_secret.arn
      BETFAIR_APP_KEY_SECRET = var.betfair_app_key_secret.arn
      UK_HTTPS_PROXY_SECRET = var.uk_https_proxy_secret.arn
      ARBRIVER_BUCKET = "arbriver-bucket"
    }
  }
}