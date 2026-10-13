variable "aws_region" {
  description = "Region of the AWS project. Fixed by AWS for this account type."
  type        = string
  default     = "us-east-2"
}

variable "aws_profile" {
  description = "AWS CLI profile to use. Sign in first with `aws login --profile jobtracker`."
  type        = string
  default     = "jobtracker"
}
