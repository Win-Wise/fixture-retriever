# Create a Log group for the state machine
resource "aws_cloudwatch_log_group" "MySFNLogGroup" {
  name_prefix       = "/aws/vendedlogs/states/MyStateMachine"
  retention_in_days = 1
  lifecycle {
    prevent_destroy = false
  }
}