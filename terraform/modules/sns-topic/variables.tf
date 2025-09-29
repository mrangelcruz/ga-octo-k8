variable "topic_name" {
  description = "The name of the SNS topic."
  type        = string
}

variable "email_subscribers" {
  description = "A list of email addresses to subscribe to the SNS topic."
  type        = list(string)
  default     = []
}
