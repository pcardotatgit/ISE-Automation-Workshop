# Cisco Identity Service Engine API Labs

The resources in this repo are mainly the python scripts examples used for the an ISE Automation Workshop.

Topics covered are :

- ISE ERS APIs
- ISE pxGrid REST APIs
- ISE pxGrid Websockets
- ISE pxGrid Direct
- XDR ISE Automation workflows
- Custom Splunk APP for ISE

A lot of these resources are still under contruction

# Introduction ISE APIs ( don't hesitate to skip that part )

When we talk about APIs , generaly spealing we talk about automation.

Cisco Identity Service Engine is one of the most complex solution to automate, because ISE does not only expose standard open APIs, but ISE offer as well another way to integrate ISE services in the IT world. This technology is pxGrid.

ISE Open APIs are straigth forward to use. We just have to send API call to an API URL Endpoint and use an API_Admin username and password. EASY !!!

In  the oposite pxGrid requires first pxGrid client to identify themselves to the ISE server which is managing pxGrid services, which will allow them to talk to ISE. Second pxGrid clients have to register to what we call pxGrid topics, which are the services to consume and if we do a comparison with other things, which act as messaging spaces where subscribers will be able to follow conversations on a specific topic. Subscribers are able to see every messages sent by publishers, and can do something with it. This conversation mechanism allows to share data among publishers and subscribers in real time, instantly with no delay. 

ISE server is responsible for managing the whole pxGrid service, and act at the same time as a subscriber and a publisher.

The underlaying technology used to manage this pxGrid part is websocket which gives a real time bi directionnal communication service between clients and server that first authenticate themselves with each other.

We understand that pxGrid is more complex to setup but the benefits of this for sure is that this technology is natively much more secure, robust and scalable than standard open APIs. pxGrid is a perfect technology for machine to machine communication. It has been created for this.

At the same time, pxGrid offer for every pxGrid topics Open APIs, in parallel to websockets. We can consume these APIs the same ways as standard APIs, with the difference that in order to be able to send API Calls to a pxGrid Topic, pxGrid client have to authenticate themselves to ISE, second register to a pxGrid topic when retreive a dynamically generated secret ( which act as an API key ) and use this secret in every API calls. VERY VERY secure !!! with 3 levels of authentication. 

We can add to that, the fact that usernames and passwords for client authentication is allowed but not recommended ! The recommended authentication method is certificat.

Okay having said that we understand that a pxGrid Setup is complex and is probably too much for a lot of basic use cases.

But is the today IT and OT worlds ! Machine to Machine communication is the normal. We don't see only humans behind their laptop consuming the IT resources available in the network. We talk about thousand of devices talking to each other on demand on every direction, wich is today a true nightmare for security !  It is very difficult to keep control on what happen.

Identify Service Engine control at every entry point of the network, Users and the machines they use, but Applications and processes within workloads as well. And we can include agents in this second category.

Identity Service Engine is already ready to address threats brought by AI agents by controling their access to the network.

# The goal of this Workshop 

The goal of this workshop is to offer a guided fast path to programmers who want to learn about ISE Automation with no delay and a minimum of complexity. Which is a big challenge when we talk about Cisco ISE automation. I hope that I was able to reach that goal.

This workshop content is based on the works done by Thomas Howard, Victor Bovbrov and Tailor cooks. Thanks a lot to you guys for the amazing documentation you created. I just took your workshops and code, and just put them into my own format and I re organized them into a logical agend. The documentation you created guys was perfect for me, to help me to understand with no effort how to do the things !

## References I used :

- [working with pxGrid 2.0](https://www.youtube.com/watch?v=UVQr9o0TN0c) 
- [Introduction to the Cisco Platform Exchange Grid in ISE ](https://www.youtube.com/watch?v=_aO6oZrYCPE)

Pre requist ... You know what is a REST API,you  are familiar with JSON format, and you already talk python.

# Few words about Labs

All these labs use the same use case which is very representative of the ISE automation capability.

This is the ANC Use Case. Adaptative Network Containement is a feature of ISE which allows adminstrators to exclude Endpoints out of the network for any good reasons like the Infection of this Endpoint. 

This feature has a dedicated GUI in ISE which allows to create ANC policies ( QUARANTINE, PORT BOUNCE, Re AUTHENNTICATE, SHUTDONW ) and which allows to add endpoints to these policies by their current IP addresses or by their Mac Address.

It was great to make this native capability of ISE a "Click and Go" feature as it helps to go very fast on host isolation whenever it is needed.

It was great as well to expose dedicated APIs for this feature that allow to completely automate it. 

Host isolation of host infected by malwares or ransomwares can be achieved instantly when the infection is detected.

So goal for every labs will be to automate ANC.

## You need an ISE Lab.

A straight forward solution if you want to avoid to setup your self an ISE lab which requires an lot of things to setup, is to use Cisco DCLOUD whan you are a Cisco Partner.

Here are the 2 labs recommended to you :

- **Cisco ISE 3.4.5 Enterprise and Security Integrations**
- **Cisco Secure Network Analytics 7.5.3 Test Drive v1.0**

These 2 labs gives you complex network environment with a lot of machines and servers already installed. These 2 lab heavily use Cisco ISE. You can use some of the labs guides attacheds to these lab to prepare and roll out example of Device Access Control and Device Isolation. And you can bring your own demo which is the option  we will use with the python scripts we have in the API Lab, will will run in the JUMPHOST.

Connect your personnal lab laptop to DLCOUD labs thanks to VPN is the best option. This option gives you a strng capability to extend your security scenarios.

## Install the python scripts

We have several labs which use python scripts. That means that for every lab you have to install these python.

These python script can run on Windows, Linux or Mac Machines... This is python.

But these lab scripts are packaged in a way that allows theirs installation in less than 2 minutes on windows machines. The only prerequisit on the windows machine is to have python windows installed.

JUMPHOST Machines in DLCOUD Labs are ready. That means that you can just go to the installation.

### Fast installation on windows machines.

Download the lab scripts into a working directory into your laptop. Unzip the dowloaded file and open a terminal console into the project root directory. Then

- type **a**

- then type **b**

- then type **c**

- then type **d**

- finally type **e**

Okay. Installation is done... It takes only 2 minutes and the JUMPHOST in DCLOUD labs is ready to be used with no addtionnal setup for this procedure.

Now, whenever you want to run the script in the selected lab, you have to open a CMD console in the script directory, then type the letter **a** to start the python virtual environment and then run the required python scripts.


# Lab 1 - ERS APIs

ERS ( Extend REST Services ) are the legacy REST APIs exposed by ISE. They are just the old Open APIs exposed by ISE. 

These APIs are still there, available in the server, very easy to use so why not using them.

The API documentation is available directly on the server Web GUI, and available in Cisco DevNet : [ERS APIs](https://developer.cisco.com/docs/identity-services-engine/latest/ers-api/)

Authentication is based on either username and passwords of a specific ERS Administrator we have to create in the ISE Server, or on certificates we have to install in ISE and in the python REST Client.

In order to make things fast and straight forward we use username and password in these labs.

First step is to create an ERS API full Administrator in ISE. Check that ERS services are enable.

Edit the **config.json** file and udpate the empty variables.

Now run the scripts one after the other and check the results either in the script console, or in the ISE server.

We start by interacting with ISE thanks to a few APIs calls, and then we add an endpoint into an existing ANC Policy.

Review the Python code, and you will see how we progress. We start with a straight forward API static API, and we move script after script to a generic API call python function which is a single function to use fo any API calls we want to send to any REST Solution. This function just expect variables as input that are used to Customize the API call. And we store the JSON result as text files into the **./results** subfolder.

# Lab 2 - OPEN APIs

Exactly the same as the ERS API lab, but then we use the ISE Open APIs which are the modern version of ISE REST APIs.

You already know the principle, this is the same as ther ERS Lab.  For the example we only run one API call.

But feel free to use anyother API call you can find in the [ ISE Open API documentation ](https://developer.cisco.com/docs/identity-services-engine/latest/open-api/).


# Lab 3 - pxGrid REST APIs

As said in the introduction, pxGrid is complex, but absolutely powerful and natively secured.

pxGrid offer 2 services for every pxGrid topics, which are websocket services and REST APIs.

Let's start with pxGrid REST API which are quite simple to use. They work the same as standard Open APIs with the difference that we must first register our pxGrid Client to ISE and second we must subscribe to topics. 

Once done we are able to retrieve a secret our python client can use in the API calls.

Installation of the scripts is the same as usual. 

Once the python virtual environment has been created and python module installed, edit the **config.json** and **config_pxgrid.json** file and udpate the variables.

In ISE check that pxGrid is enabled. And we have to enable username/password based client authentication. ( once again, use go straight forward and dont use certificate based authentication ). Check in ISE that some pxGrid services are published and available to pxGrid clients. For this lab we the the com.cisco.ise.session, com.cisco.ise.config.anc topics.

First we just test that the API connection to ISE is Okay

Second we use pxGrid APIs to create a new pxGrid user in ISE. Once you run the script, then the new user appears in ISE pxGrid clients table, in the pending state. You have to approve it manually  in the ISE GUI in order to allow it to consume pxGrid Services. 

Once the new user approved, then you can consume the pxGrid services.  You run the other python scripts one after the other, Check result eithet in the python console, or in ISE GUI.

The final goal is to QUARANTINE an Endpoint thank to pxGrid API REST Calls 

# Lab 4 - Automate Endpoint isolation from infection detection by Network IPS

This lab is summarizes previous labs. At this stage we know how to consume ISE APIs for the ANC use case.

Now let's do it for real, exactly like we would want to deploy an Isolation service in oour network.

If we discover an infected Endpoint thanks to any detection solution, then we want to automatically exclude it out of the network.

We can use the **Cisco Secure Network Analytics 7.5.3 Test Drive v1.0** DLCOUD lab to reproduce completely this scenario, but instead of doing that, let's use a custom syslog server and let's send to it syslog Cisco Secure Firewall IPS messages that alert about an internal IP address that is sending XSS and SQL Injection Attacks to internal Web Server.

This kind of alert is what we can call an High fidelity alert which confirms us that we have an infected machine. And then the priority become to exclude it out of the network.

We use a separate syslog generator which send real syslogs from Cisco NGIPS we saved into a text file which is read and sent by the syslog generator.  Thanks to this tiny component , we don't need to setup the a real attacks. But once again, the DLCOUD lab mentionned prior allows to reproduce this attack for real.

Your challenge in this lab is to detect the attack in real time directly in the syslog server, and thanks to a python function you have to write, you must to add the infected internal machine to a QUARANTINE ANC policy. 

## Roll out the Lab

Pre requisit for this lab : You have done Lab 3.  Copy the **z_pxgrid-creds.txt** file created by scripts in Lab 3. You will have to paste it in the **demo_syslog_server** working directory.

- First step, let's identify in ISE an Endpoint we could use for the demo. The goal is to get close to a real life scenario. So from the ISE Operation => live Session, identify an host in session which has an IP address ( the host must have an IP address ).

Copy the IP address of this host. We need it to setup our demo data.

- Second, deploy the **demo_syslog_generator**. Same procedure as usual then from the terminal console open into the working directory you selected for it and start with the **0-create_syslog_file.py**.
    - run it and when asked type the IP addess you selected before from ISE Live Logs
    - Okay ready. Don't close the console
    
- Step 3 : deploy the **demo_syslog_server**, into python virtual environment and just run it. You are supposed to see it waiting for syslogs. Paste the **z_pxgrid-creds.txt** file created by scripts in Lab 3 in the in the **demo_syslog_server** working directory.

The syslog server is a very basic tools packaged for the demo. Don't hesitate to review the code, it is quite easy to understand.

You will see into the code the syslog server part, the Cisco FTD IPS logs parser part and the ISE Quarantine part.

For information, I was able to use it in heavy loaded labs environments , and it works very well with a lot of power. It is not only a gadget for demo.

- Step 4 , come back to the **demo_syslog_generator** console and run the **1-send_syslog_from_syslogs_text_file.py**

You are supposed to see parsed syslog messages arriving in the **demo_syslog_server** console. When the syslog demo file has been completely sent, then the syslog server displays the list of Attacker IP addresses discovered in logs followed by result of operation for adding the infected IP address you selected prior.

You can check in ISE ANC Policy Endpoint Assignment that this IP address is now part of the Quarantined enpoint.

**Notice ! ** for successful QUARANTINE, as we use the IP address as the endpoint identifier, the ip address must have a current session in ISE, because ISE check this to execute the assignment to QUARANTINE.

If you have look to the syslog server code you will recognize the **7_pxgrid_add_end_point_to_anc_policy.py** from lab_3. We just packaged it a little bit for this current lab.

You must update the variables in **config_pxgrid.txt** in order to grant the API interaction with ISE. 

The script is now named **pxgrid_add_end_point_to_anc_policy.py** and is imported as an external resources into the syslog server python code. It is now a re usable component, the function it contains can be called directly from the syslog server script.

It is now customized to handle IP addresses instead of mac addressses.


# Lab 5 - Use Webex Chat Bot to receive alerts on a phone and trigger Endpoint isolation

This lab is just here to complete the Lab 4 scenario with an addtional alerting system which brings as an approval process in order to involve Security Administrators in the endpoint isolation process.

Here, we just add a Webex Bot logic to our syslog server that will send an alert to Security Administrator every time an infected machine is detected. 

Thanks to this, administrators will be aware of a threat in real time, and they will be able to confirm the host isolation from the alet formular.

In this lab you just have to deploy a new version of the syslog server which includes a webex bot logic, and use it. 

Instruction are shared to link this bot logic to what has been done before.

We don't details in this lab how the bot logic is built. Because these details are already documented in the Webex Alerting system project in this github.

[Build a Webex advanced alerting system](https://github.com/pcardotatgit/webex_for_xdr_part-1_card_examples)

# Lab 6 - Automate host isolation thanks to Cisco XDR Automation

In this lab we use XDR Workflows instead of using python scripts. The result must be the same as Lab 6 but completely managed by Cisco XDR.

under contruction

# Lab 7 - Automate host isolation thanks to Event Based Detections in SPLUNK

In this lab we replace our custom syslog server by splunk. Our final goal remains the same.

We leverage Event Based Detection and Custom Splunk APPs

under contruction

# Lab 8 - Manage certificates for authentication

Let's move forward thru this lab, now we continue on studying pxGrid websockets use cases.

And before that it is time to address the Certificats exchange for authentication which is mandatory for the next steps.

code under contruction

# Lab 9 - STOMP Lab

STOMP ( Simple Text Oriented Messaging Protocol ) is messaging system which uses a simple and straigth forward communication protocol. 

In a STOMP architecture a server manages the messaging service and clients will establish persistent connection to the server. Clients will be publishers ( clients wich send messages ) and subscribers ( clients that listen to messages ).  Messages are sent to separate spaces named topics which are nothing more than messages queue dedicated to specific topics. 

STOMP is the technology used by pxGrid for data exchange. ISE pxGrid publishers use STOMP over websocket to share their data with pxGrid subscribers, and ISE hosts the STOMP service.

At the same time, ISE is a publisher and a subscriber which are using the STOMP services

This lab just help to understand how it works, and it is a very good introduction to pxGrid websocket services

[Access to the Lab](https://github.com/pcardotatgit/ISE-Automation-Workshop/tree/main/ISE_APIs_Lab-10_STOMP_Lab)

# Lab 10 - WebSocket Lab

Websockets is a bi directionnal communication channel between clients and servers which is based on a connected mode.

That means that in order to make the client and the server to talk together, we must first established a connection from the client to the server and of course manage authentication. 

The server is supposed to authenticate the client and acknowledge the connection. 

Once done the client and the server are able to send messages to each other. At any time and in both directions. Messages sent are received instantly in real time.

Websockets are perfect as a communication layer for chatting applications. 

Among the benefits this technology brings we have the capability to easily make clients that are behind firewalls in the internal network, to talk with a central server which is on the public INTERNET. We can imagine how large the scope of application is and how security control is important as well.

Another benefits is the capability to use a web browser as a client as websockets connection can be managed by javascript.

In ISE, Websockets is the underlaying communication channel used by the ISE STOMP architecture to allows pxGrid Clients to interact with ISE.

Once the communication established client and server must use communication rules to communicate together. pxGrid relies on the STOMP ( Simple Text Oriented Messaging Protocol ) messaging services for this.

This lab aims to get you familiar with websockets. 

Deploy the scripts located into the **ISE_APIs_Lab-9_websocket_lab** subfolder.

Installation is the same as usual.

First activate the python virtual environment and run the **1-websocket_server.py**

Second, activate in a second time the same python virtual environment in a second terminal and then run the **2-websocket_client.py**

You are supposed to see a connection between the client and the server, then you can chat.

Review the python code to understand what we do.  We need the **websockets** and the **asyncio** python modules.

# Lab 11 - pxGrid websocket Lab

Okay, at this stage we understand every layer underneeth pxGrid. it is time to use it.

Let's put everything together and let's write our custom pxGrid client.


under construction

# Lab 12 - pxGrid Direct Lab

under construction

# Lab 13 - pxGrid CLI

under contruction

 
# Lab 14 - MCP Server for ISE

under contruction


# resources 

In this section some references to not miss :

