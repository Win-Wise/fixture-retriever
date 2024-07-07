resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "fixture-retriever-statemachine"
  role_arn = aws_iam_role.StateMachineRole.arn
  definition = templatefile("${path.module}/statemachine.asl.json", {
    ProcessingLambda = var.processing_lambda.lambda.arn
  }
  )
  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.MySFNLogGroup.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }
}