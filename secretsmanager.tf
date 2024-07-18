resource "aws_secretsmanager_secret" "betfair_password" {
  name = "betfair_pass"
}

resource "aws_secretsmanager_secret_version" "betfair_password" {
  secret_id     = aws_secretsmanager_secret.betfair_password.id
  secret_string = var.betfair_password
}

resource "aws_secretsmanager_secret" "betfair_app_key" {
  name = "betfair_app_key"
}

resource "aws_secretsmanager_secret_version" "betfair_app_key" {
  secret_id     = aws_secretsmanager_secret.betfair_app_key.id
  secret_string = var.betfair_app_key
}

