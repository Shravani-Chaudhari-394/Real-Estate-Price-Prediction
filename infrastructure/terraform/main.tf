provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "ap-south-1"
}

resource "aws_instance" "api_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  tags = {
    Name        = "real-estate-api"
    Environment = "production"
    Project     = "capstone"
  }
}

resource "aws_db_instance" "postgres" {
  identifier     = "real-estate-db"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  username       = "postgres"
  password       = var.db_password
  skip_final_snapshot = true

  tags = {
    Environment = "production"
  }
}

variable "db_password" {
  sensitive = true
}
