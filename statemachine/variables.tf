variable "processing_lambda" {
  type = any
  description = "the processing lambda"
}

variable "populator_lambda" {
  type = any
  description = "the populating lambda"
}

variable "statemachine_role" {
  type = any
  description = "execution role for statemachine"
}