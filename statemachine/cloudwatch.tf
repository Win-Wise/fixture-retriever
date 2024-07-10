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
  schedule_expression = "cron(0 0/8 * * ? *)"
  description         = "trigger the fixture retriever step function"
}

resource "aws_cloudwatch_event_target" "step_function_event_target" {
  target_id = "trigger-fixture-retriever"
  rule      = aws_cloudwatch_event_rule.step_function_event_rule.name
  arn       = aws_sfn_state_machine.sfn_state_machine.arn
  role_arn  = aws_iam_role.event_bridge_role.arn
  input     = jsonencode({
    days_forward: 20,
    books: [
      "CAESARS",
      "DRAFTKINGS",
      "FANDUEL",
      "BETRIVERS"
    ]
  })
}

data "aws_iam_policy_document" "eventbridge_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

resource "aws_iam_role" "event_bridge_role" {
  name               = "eventbridge-populator-role"
  assume_role_policy = data.aws_iam_policy_document.eventbridge_assume_role_policy.json

}

resource "aws_iam_policy" "eventbridge_policy" {
  name   = "eventbridge-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      },
      {
        Action : [
          "logs:CreateLogDelivery",
          "logs:CreateLogStream",
          "logs:GetLogDelivery",
          "logs:UpdateLogDelivery",
          "logs:DeleteLogDelivery",
          "logs:ListLogDeliveries",
          "logs:PutLogEvents",
          "logs:PutResourcePolicy",
          "logs:DescribeResourcePolicies",
          "logs:DescribeLogGroups"
        ],
        Effect : "Allow",
        Resource : "*"
      },
      {
        Action: [
          "states:StartExecution"
        ],
        Effect: "Allow",
        Resource: [
          aws_sfn_state_machine.sfn_state_machine.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eventbridge_policy_attachment" {
  role       = aws_iam_role.event_bridge_role.id
  policy_arn = aws_iam_policy.eventbridge_policy.arn
}
