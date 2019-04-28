provider "aws" {
  access_key = "${var.AWS_ACCESS_KEY}"
  secret_key = "${var.AWS_SECRET_KEY}"
  region     = "${var.AWS_REGION}"
}

resource "aws_security_group" "twitter-trends" {
  name        = "twitter-trends"
  description = "Allow traffic from my IP address."

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["${var.MY_IP}"]
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
  instance_type = "m5.large"
  key_name   = "${var.AWS_KEY_NAME}"
  security_groups = ["twitter-trends"]

  provisioner "file" {
    source = "setup_docker.sh"
    destination = "setup_docker.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo chmod +x setup_docker.sh", "sudo ./setup_docker.sh"
    ]
  }

  connection {
    user = "ubuntu"
    private_key = "${file("${AWS_PRIVATE_KEY}")}"
  }

}
