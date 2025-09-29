terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  # Load the topic definitions from the YAML file.
  topics = yamldecode(file("${path.module}/../../config.yaml")).topics
}

module "sns_topics" {
  for_each          = local.topics
  source            = "../modules/sns-topic"
  topic_name        = each.key
  email_subscribers = each.value.email_subscribers
}

resource "aws_iam_user" "sns_publisher" {
  name = "sns-publisher"
}

data "aws_iam_policy_document" "sns_publish_policy" {
  statement {
    effect = "Allow"
    actions = [
      "sns:Publish",
    ]
    resources = [for topic in module.sns_topics : topic.topic_arn]
  }
}

resource "aws_iam_policy" "sns_publish_policy" {
  name   = "SNSPublishPolicy"
  policy = data.aws_iam_policy_document.sns_publish_policy.json
}

resource "aws_iam_policy_attachment" "sns_publish_attachment" {
  name       = "sns-publish-attachment"
  users      = [aws_iam_user.sns_publisher.name]
  policy_arn = aws_iam_policy.sns_publish_policy.arn
}
