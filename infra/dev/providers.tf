# Long-lived dev resources that stay up while the app runs locally (the Cognito
# user pool). Kept separate from the Phase 6 EKS stack so `terraform destroy`
# there never wipes the dev users.

terraform {
  required_version = ">= 1.15"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      # 6.23+ can read credentials from `aws login`
      version = "~> 6.23"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      Project     = "job-application-tracker"
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}
