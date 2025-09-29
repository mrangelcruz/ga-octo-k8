#
# Input Variables for AWS Infrastructure
#

variable "aws_region" {
  description = "AWS region where resources will be provisioned."
  type        = string
  default     = "us-west-2"
}

variable "account_id" {
  description = "AWS Account ID where resources will be provisioned. This is typically passed in via a .tfvars file."
  type        = string
  nullable    = false
}
