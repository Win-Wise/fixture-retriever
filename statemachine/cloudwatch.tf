# Create a Log group for the state machine
resource "aws_cloudwatch_log_group" "MySFNLogGroup" {
  name      = "/aws/vendedlogs/states/fixture-retriever-statemachine"
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}