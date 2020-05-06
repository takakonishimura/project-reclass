provider "aws" {
  profile = "default"
  region = "us-east-2"
}

data "template_file" "user_data" {
  template = "${file("./scripts/user_data.sh")}"
}

resource "aws_instance" "new_resource" {
  ami = "ami-0fa12c0e9a9857e60"
  instance_type = "t2.micro"
  key_name = "toynet-2020"
  user_data = data.template_file.user_data.rendered
}
