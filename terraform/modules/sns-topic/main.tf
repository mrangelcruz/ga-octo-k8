resource "aws_sns_topic" "topic" {
  name = var.topic_name
}

resource "aws_sns_topic_subscription" "email_subscription" {
  for_each  = toset(var.email_subscribers)
  topic_arn = aws_sns_topic.topic.arn
  protocol  = "email"
  endpoint  = each.value
}
