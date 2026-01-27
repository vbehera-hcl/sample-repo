# Terraform configuration for Nautilus EC2 Web Server

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1" # Change to your preferred region
}

# Data source to get the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# Security Group to allow HTTP traffic on port 80
resource "aws_security_group" "nautilus_web_sg" {
  name        = "nautilus-web-sg"
  description = "Security group for Nautilus web server allowing HTTP traffic"

  # Inbound rule for HTTP traffic
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rule to allow all traffic (required for package installation)
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "nautilus-web-sg"
  }
}

# EC2 Instance with Nginx user data
resource "aws_instance" "nautilus_ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.nautilus_web_sg.id]

  # User data script to install and start Nginx
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y nginx
              systemctl start nginx
              systemctl enable nginx
              EOF

  tags = {
    Name = "nautilus-ec2"
  }
}

# Output the public IP address of the instance
output "instance_public_ip" {
  description = "Public IP address of the Nautilus EC2 instance"
  value       = aws_instance.nautilus_ec2.public_ip
}

# Output the public DNS of the instance
output "instance_public_dns" {
  description = "Public DNS of the Nautilus EC2 instance"
  value       = aws_instance.nautilus_ec2.public_dns
}

# Output the instance ID
output "instance_id" {
  description = "ID of the Nautilus EC2 instance"
  value       = aws_instance.nautilus_ec2.id
}
