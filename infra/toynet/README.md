# Introduction

### Tools

[Terraform by HashiCorp](https://www.terraform.io/) is a tool for building, changing, and versioning infrastructure. Terraform is fully integrated with cloud service providers (AWS, Openstack), configuration management tools (Chef, Puppet), and third party providers (Cloudlfaire, DNSimple). We describe a state to Terraform and it generates an execution plan to achieve this state. As configurations change, Terraform determines the minimal incremental execution plan.

[Packer by HashiCorp](https://www.packer.io/) is a lightweight open source tool for creating identical machine images for multiple platforms from a single source configuration. It can also integrate with configuration management (Chef, Puppet).

In ToyNet, we install mingrammer's `Diagrams` on top of `Ubutu 18.04`. Packer brings up an EC2 instance of the Ubuntu image. The first shell script halts execution until the EC2 instance has finished system updates before executing the next shell script which installs `graphviz` and `python3-pip` as underlying dependencies to the `Diagrams` Python Package. Packer automatically terminates the EC2 instance and registers the new AMI with your account.

* What is the desired architecture (include visuals)?

### Longerm Orchestration Plans

* What is Docker

# Making Changes

### Updating the AMI

1) Update `infra/toynet/terraform/toynet.json` provisioning scripts.

2) Build new Packer Image by running: `packer build toynet.json` in `project-reclass/infra/toynet/packer/`  with final output that looks like:

    `==> Builds finished. The artifacts of successful builds are:`
    `--> amazon-ebs: AMIs were created:`
    `us-east-2: ami-036ded237fa2772c7`

3) Grab AMI identifier from the final line of the console logs.

4) Define `ami_id` to `infra/toynet/terraform/devUsers.tfvars`.

5) Announce update to engineers or log into all currently running instances to save their WIP to Github (the change affects the state of all instances and thus they will be destroyed and recreated with new base image).

6) Run `terraform apply -var-file="devUsers.tfvars"` in `project-reclass/infra/toynet/terraform`.

### Spinning up a new instance for new user

1) Update `infra/toynet/terraform/devUsers.tfvars`:

    * add `Name` tag you want for your new instance to `instance_names` (convention is `toynet-<developer first name>`)
    * increment `instance_count` by 1 (Terraform state will have this many instances whose `Name` tags are pulled from `instance_names`)

2) Run `terraform apply -var-file="devUsers.tfvars"` (a new instance will be created for all new `instance_names`, any old instances no longer in the list will be destroyed).

3) Setup AWS access:

    * Create new IAM role
    * Send username and temporary password to new developer.
    * Send PEM file to new developer using PrivNote.

5) On new developer's machine:

    * Create new AWS password
    * Add home IP addtess to security group on TCP Port 22
    * Grab hostname of new instance from AWS console
    * Install VSCode and set up SSH configurations
    * SSH with them and provide them [Getting Started Tutorial](https://github.com/takakonishimura/project-reclass/blob/master/toynet/ONBOARDING.md)
