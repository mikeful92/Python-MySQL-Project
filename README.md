# Card Project

## Set-up

### Server

This project will be running on an AWS EC2 instance. I have selected a Ubuntu 14.04 LTS Operating System(OS), and the commands through out the set-up will be based on that. If another OS is used, the commands could differ.

I will presume knowledge on how to create an instance and how to access it using SSH. You can follow any basic tutorial or guide.

One thing that we will need is two new inbound rules added to the security group. You can click "Security Groups" under "Networking & Security" on the right side bar. The right click on the specific Security Group for your instance, and select "Edit inbound rules".

The first rule will be type HTTP, there is no need to edit any other part of it. We can let the source be Anywhere.

The second rule will be "Custom TCP Rule", Port Range "8080", Source "Anywhere". This rule will alow us to use port 8080 to test our server from our local computer's browser.

### Software

We can start with two commands for our new instance to make sure that it is up to date.

```
$ sudo apt-get update
$ sudo apt-get dist-upgrade
```

(Press "Y" when prompted)

Next we will install two programs we need.

```
$ sudo apt-get -y install apache2 & mysql-server
```

Apache2 will be our web server that handles all incoming requests on port 80. It will also help us server static files. 

MySQL will be our Database. During the instalation process it will ask you to type in a new password for the root user. 
We can log into MySQL using the following command.

```
$ mysql -u root -p
```

Next it will ask you to type the password you assign and press enter.

At this point we can create the "bb_cards" database that will be used in this project.

```
mysql> CREATE DATABASE bb_cards;
quit
```

The creation of the Tables and insertion of data will be accomplish later.

In order for Python to talk to the Database we need a connector. While there are various available, we will by using PyMySQL.

We will confirm that we have the correct version of Python.

```
$ python3 -V
Python 3.4.3
```

First we need pip installed. Pip is the Python package manager that will allow us to install the needed connector.

```
$ sudo apt-get install python3-pip
```

After pip has been installed we can install the module

```
$ sudo pip3 install pymysql
```

Next we will need Git to clone all the files.

```
$ sudo apt-get install git
```

Clone this repo

```
$ git clone https://github.com/mikeful92/Python-MySQL-Project.git
```


Now we are ready to start with Phase 1

## Resouces

Amazon AWS: https://aws.amazon.com/

AWS Guide: http://www.crmarsh.com/aws/

Apache2: https://httpd.apache.org/

MySQL: https://www.mysql.com/

Python Documentation: https://docs.python.org/3/

Pip: https://docs.python.org/3/installing/index.html?highlight=pip

PyMySQL Module: https://github.com/PyMySQL/PyMySQL
