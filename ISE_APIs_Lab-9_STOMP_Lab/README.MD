# STOMP Lab

This lab aims to get you familiar with the STOMP architecture which is used by ISE pxGrid.

STOMP is a simple and very efficient messaging system which is used by pxGrid Services.

Entities involved into ISE pxGrid use space queues named topics to exchange information with each other.

In this concept we have entities that publish information into topics, entities who susbcribed to the topics will see everything that is published and will be able to do things with it. Entities can be only publishers, or only susbcribers or both. 

And we have a central server which managing the messaging service, authorize entities to subscribed to topics and manage topics the messaging queues.

We will play with all this in this lab

The architecture of our lab contains  :

- a STOMP server which manages a messaging service
- a publisher which send messages to Message queues ( a topic ).
- a subscriber which will subscribe to the same topic as the publisher and which will be able any messages sent by the publisher.

# Setup the server

Let's use CoilMQ which is a fast to STOMP server from the python community. This one is very straight forward to install.

[CoilMQ getting started](https://github.com/hozn/coilmq/wiki/Getting-Started)

CoilMQ installation is very simple, follow the here under steps

Create a working directory and open a terminal console into this directory

( I assume that you know how to execute the following instruction on your python machine. On windows machine you can type, a then b , c , d and e )

- Create a python virtual environment 

- activate this python virtual environment

- Install the CoilMQ python module

    **pip install CoilMQ**
    
- We are ready to go. you can just start the CoilMQ server :

    **Just type : CoilMQ -b 0.0.0.0 -p 61613**
   
The server starts and listen on localhost on port 61613.  ( You will probably have to Authorize the Application in the workstation Firewall, a windows popup is supposed to appear. Then authorize the application )

( notice : CoilMQ can use default settings you can change by editing the coilmq.cfg file in the Lib/site-packages/config folder of the python virtual environment ).

The server is now waiting for connections from publishers and subscribers.

# Now let's install a STOMP publisher

We can use python script for this, but once again we are going to use a ready to use package from the python community. A STOMP Client module [stompl.py]( https://jasonrbriggs.codeberg.page/stomp.py.pages/quickstart.html)

Here are the installation steps :

- create another working directory and create a python virtual environment into it. Or you can open a second terminal and activate the python environment ( type : a )
- Install the stomp client python module , from a terminal console open into this second working directory.

    **pip install stomp.py**
    
We are ready to go and we can test our setup at this stage thank to STOMP CLI client we just installed

- Within the terminal console type :

    **stomp -H localhost -P 61613**
    
You are supposed to see the prompt changing to **>** ( greater than ), meaning that the session is started on the STOMP server and you can send commands.

- Now type :

    - **subscribe /queue/test**
    
    - **send /queue/test hello world**
    
You probable understand what we do here. First We subscribe to a queue named **queue/test** and Second we send the "hello world" message into it.

- Our Stomp Client is still connected you can type :

    **help** 
    
This command display the STOMP commands we can execute. And we see that the set of commands is very basic. Largely enough for what we want to do.

We can move to the next step. Now Let's use a python as STOMP publisher.

The python script named **publisher_send_message.py** is an example of quick and dirty STOMP publisher. Open it a review it.

You should be able to easily understand what it does. We have a python class which manages STOMP services. 

- We start STOMP Services

- Authenticate and Connect to the central server

- We subscribe to an existing topic

- We send a message to it

- We wait 2 second and we disconnect

This python script doesn't stay connected to the STOMP server.

The [STOMP publisher instructions]( https://twiki.cern.ch/twiki/bin/view/EGEE/MsgTutorial ) gives good explanations about how it works.
Have a look to the section which describe the Listener. We see the instructions needed to establish the connection with the STOMP server and we understand that we have to setup a listener class which manages events like receiving messages.

So we understand that once connected to the server and subscrided to a topic ( a Queue ) our STOMP client is watching this Queue and monitors every messages that will come into it. The **def on_message(self, headers, body):** of this class will capture every messages sent ot the queue in the **headers** and **body** variable, then we will be able to compute them inside this function.

Don't exit from the CLI STOMP Client we started prior, we will use it later. 

Open a third terminal console into the same working directory and activate again the python virtual environment.

- Run the **publisher_send_message.py** script. 

    **python publisher_send_message.py Hello World**
    
The expected result is to see in the python console the message : **received a message "Hello World"**.

This message actually comes from the queue in the STOMP server and you probably understand that our **publisher_send_message.py** script is acting at the same time as a publisher and a subscriber. But we see that connection is closed just after having sending the message.

# Setup the subscriber

**STILL UNDER CONSTRUCTION**

Our final goal is to have several subscribers located in separte locations, that will see messages sent by publishers.

**Option 1**

We already have one subscriber which is the CLI STOMP Client we used prior.

Go back to it, or open again a terminal console and activate the python virtual environment.
Then connect again and suscribe to the /queue/test topic exactly as we did prior. Then wait for messages

**Option 2**

Have a look to the **subscriber.py** python script.

Repeat the installation step used for the publisher and run **subscriber.py**. 

The script is waiting now for messages.

**Send Message to the messages queue**

Go back to the publisher and then send a new message to the Queue. 

The expected result is to see this message in the subscriber console.

Every suscribers connected to the same topic will see the same message at the same time, in real time.



