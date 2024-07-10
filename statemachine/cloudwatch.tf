# Create a Log group for the state machine
resource "aws_cloudwatch_log_group" "MySFNLogGroup" {
  name      = "/aws/vendedlogs/states/fixture-retriever-statemachine"
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_cloudwatch_event_rule" "step_function_event_rule" {
  name                = "trigger-fixture-retriever"
  schedule_expression = "cron(0 0/12 * * ? *)"
  description         = "trigger the fixture retriever step function"
}

resource "aws_cloudwatch_event_target" "step_function_event_target" {
  target_id = "trigger-fixture-retriever"
  rule      = aws_cloudwatch_event_rule.step_function_event_rule.name
  arn       = aws_sfn_state_machine.sfn_state_machine.arn
  role_arn  = aws_iam_role.StateMachineRole.arn
  input     = jsonencode({
    days_forward: 20,
    books: [
      "CAESARS",
      "DRAFTKINGS",
      "FANDUEL"
    ]
  })
}