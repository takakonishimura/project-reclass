# Introduction

[High Fidelity Visualization of how we use Terraform and Packer](https://docs.google.com/presentation/d/1fWdFEkkNzuaBaanlJP4Dc5YfGcCB2XJ-N4KkJMSqvLc/edit?usp=sharing)!

### Tools

[Terraform by HashiCorp](https://www.terraform.io/) is a tool for building, changing, and versioning infrastructure. Terraform is fully integrated with cloud service providers (AWS, Openstack), configuration management tools (Chef, Puppet), and third party providers (Cloudlfaire, DNSimple). We describe a state to Terraform and it generates an execution plan to achieve this state. As configurations change, Terraform determines the minimal incremental execution plan.

[Packer by HashiCorp](https://www.packer.io/) is a lightweight open source tool for creating identical machine images for multiple platforms from a single source configuration. It can also integrate with configuration management (Chef, Puppet).

### Deployment Process of Developer Boxes

<span>
<kbd> <img src="/images/infra_packer.png" height=160 width=400/> </kbd>
<kbd> <img src="/images/infra_terraform.png" height=250 width=400/> </kbd>
</span>

In ToyNet, we install mingrammer's `Diagrams` on top of `Ubutu 18.04`. Packer brings up an EC2 instance of the Ubuntu image. The first shell script halts execution until the EC2 instance has finished system updates before executing the next shell script which installs `graphviz` and `python3-pip` as underlying dependencies to the `Diagrams` Python Package. Packer automatically terminates the EC2 instance and registers the new AMI with your account.

### Quick Onboarding Process

<kbd> <img src="/images/infra_ssh.png" height=250 width=220/> </kbd>

For the new developer to login to their box, all that is left is to create an IAM User for them and send them the pem file. See [Getting Started Tutorial](https://github.com/takakonishimura/project-reclass/blob/master/toynet/ONBOARDING.md).

### Future Projects

We plan to move to [Docker](https://www.docker.com/why-docker) containers. This will:
1) Decouple ourselves from AWS while still hosting on AWS
2) Allow lightweight development on desktops with while maintaining consistency across platforms
3) Increase shipping speed and reliable deployments by doing away with discrepant computing enviornments or conflicting dependencies
4) Allow for multiple instances of Mininet to run on the same machine, cutting costs without introducing risk.

# Tutorials

### Technical Requirements

To be able to interact with AWS through Packer and Terraform, you must have AWS credentials setin your enviornment.
    * If your IAM role doesn't already have AWS credentials, you can get them by going to the IAM console.
    * To setup your default AWS_PROFILE in your local enviornment, [download AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

    > aws configure
    AWS Access Key ID [None]: XXX
    AWS Secret Access Key [None]: XXX
    Default region name [None]: us-east-2
    Default output format [None]: json

You must also [install Packer](https://www.packer.io/intro/getting-started/) and [install Terraform](https://www.packer.io/intro/getting-started/) before moving on.

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

    * add `Name` tag to `instance_names` (convention is `toynet-<first name>`)
    * increment `instance_count` by 1
    
    Terraform ensures `instance_count` instances whose `Name` tags are pulled from `instance_names`)

2) Run `terraform apply -var-file="devUsers.tfvars"` (a new instance will be created for all new `instance_names`, any old instances no longer in the list will be destroyed).

3) Setup AWS access:

    * Create new IAM User under group `reclass` with password `reclass`
    * Send username and temporary password to new developer.
    * Send PEM file to new developer using PrivNote.

5) On new developer's machine:

    * Visit https://909056806605.signin.aws.amazon.com/console to create new AWS password
    * [Install VSCode](https://code.visualstudio.com/download) and [set up SSH](https://medium.com/@christyjacob4/using-vscode-remotely-on-an-ec2-instance-7822c4032cff) configurations
    * Add home IP address to security group on `TCP Port 22`
    * Grab hostname of new instance from AWS console (right click instance and select `Connect`)
    * SSH with them and provide them [Getting Started Tutorial](https://github.com/takakonishimura/project-reclass/blob/master/toynet/ONBOARDING.md)
