resource "aws_cognito_user_pool" "main" {
  name           = "jobtracker-dev"
  user_pool_tier = "ESSENTIALS"

  # People sign in with their email address. Can't be changed after creation.
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 12
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # Dev pool: allow `terraform destroy`. A production pool would use "ACTIVE".
  deletion_protection = "INACTIVE"
}

resource "aws_cognito_user_pool_client" "web" {
  name         = "jobtracker-web"
  user_pool_id = aws_cognito_user_pool.main.id

  # Browser apps can't keep a secret, so this is a public client.
  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    # Dev only: lets us get a test token from the CLI with a plain password.
    "ALLOW_USER_PASSWORD_AUTH",
  ]

  # Login errors don't reveal whether an email has an account.
  prevent_user_existence_errors = "ENABLED"

  access_token_validity  = 60
  id_token_validity      = 60
  refresh_token_validity = 30
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
}
