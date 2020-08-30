terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "ap-southeast-1"
}

resource "aws_key_pair" "test" {
  key_name   = "testkey"
  public_key = file("~/.ssh/aws_ec2.pub")
}

resource "aws_instance" "testec2" {
  key_name      = aws_key_pair.v2ray.key_name
  ami           = "ami-03b993a5a631b0050"
  instance_type = "t2.micro"

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/aws_ec2")
    host        = self.public_ip
  }

  provisioner "local-exec" {
    command = "echo ${aws_instance.testec2.public_ip} > ip_address.txt"
  }

  provisioner "file" {
    source      = "../../../requirements.txt"
    destination = "/tmp/requirements.txt"
  }

  provisioner "file" {
    source      = "../../../django_project"
    destination = "/tmp/django_project"
  }

  provisioner "remote-exec" {
    inline = [
      "yum install python3"
      "python3 -m venv shortenUrlEnv"
      "source ./shortenUrlEnv/bin/activate"
      "pip install -r /tmp/requirements.txt"
      "cd /tmp/django_project && python3 manage.py runserver 0.0.0.0:9007"
    ]
  }

}

resource "aws_eip" "ip" {
  vpc      = true
  instance = aws_instance.testec2.id
}

output "ip" {
  value = aws_eip.ip.public_ip
}
