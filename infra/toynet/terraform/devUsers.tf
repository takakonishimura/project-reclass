# input

variable "ami_id" {
  type = string
}

variable "key_name" {
  type = string
  default = "toynet-2020"
}

variable "instance_names" {
  type = list(string)
  default = ["new toynet instance"]
}

variable "instance_count" {
  type = number
  default = 1
}

# provider

provider "aws" {
  region = "us-east-2"
}

# user data

data "template_file" "user_data" {
  template = "${file("./scripts/user_data.sh")}"
}

# instantiate (1 EC2 instance per instnace_count with tag Names pulled from instance_names)

resource "aws_instance" "new_resource" {
  count = var.instance_count
  ami = var.ami_id
  instance_type = "t2.micro"
  key_name = var.key_name
  user_data = data.template_file.user_data.rendered
  tags = {
      Name = "${element(var.instance_names, count.index)}"
  }
}
