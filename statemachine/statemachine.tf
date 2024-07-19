resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "fixture-retriever-statemachine"
  role_arn = var.statemachine_role.arn
  definition = templatefile("${path.module}/statemachine.asl.json", {
    ProcessingLambda = var.processing_lambda.arn,
    PopulatingLambda = var.populator_lambda.arn
  }
  )
  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.MySFNLogGroup.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }
}