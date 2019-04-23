provider "aws" {
  access_key = ""
  secret_key = ""
  region     = "eu-west-1"
}

resource "aws_security_group" "twitter-trends" {
  name        = "twitter-trends"
  description = "Allow traffic from my IP address."

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [""]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "main" {
  ami           = "ami-08660f1c6fb6b01e7"
  instance_type = "t2.large"
  key_name   = "twitter-test"
  security_groups = ["twitter-trends"]
}
