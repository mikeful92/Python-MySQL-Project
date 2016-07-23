# Card Project - Phase 1

## Set-up

### Server

This project will be running on an AWS EC2 instance. I have selected a Ubuntu 14.04 LTS Operating System(OS), and the commands through out the set-up will be based on that. If another OS is used, the commands could differ.

I will presume knowledge on how to create an instance and how to access it using SSH. You can follow any basic tutorial or guide.

One thing that we will need is two new inbound rules added to the security group. You can click "Security Groups" under "Networking & Security" on the right side bar. The right click on the specific Security Group for your instance, and select "Edit inbound rules".

The first rule will be type HTTP, there is no need to edit any other part of it. We can let the source be Anywhere.

The second rule will be "Custom TCP Rule", Port Range "8080", Source "Anywhere". This rule will alow us to use port 8080 to test our server from our local computer's browser.

## Software

We can start with two commands for our new instance to make sure that it is up to date.

<code>sudo apt-get update</code><br />
<code>sudo apt-get dist-upgrade</code>

Next we will install two programs we need.

<code>sudo apt-get -y install apache2 & mysql-server</code>

Apache2 will be our web server that handles all incoming requests on port 80. It will also help us server static files. 

MySQL will be our Database. In order for Python to talk to the Database we need a connector. We can install it with the folllowing set of lines.

<code>wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python_2.1.3-1ubuntu15.04_all.deb<br />
sudo dpkg -i mysql-connector-python_2.1.3-1ubuntu15.04_all.deb</code>

The official mysql-connector-python can only be installed directly from their website. So we just download it and install it.

