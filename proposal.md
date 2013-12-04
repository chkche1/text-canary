# Title

CIS 192 Project Proposal

# Project Name:

text-canary

# Team 

Kuan-Ting Chen (kche@seas.upenn.edu)

# General Idea

For the final project, I would like to build a "NLP as a service" web application. The web application takes user-submitted NLP task from the web page, processes the texts, and returns the results to the user. There are two components to this project: the frontend web application and the backend processing system. The backend processing system is basically going to be a distributed job dispatcher that breaks down the task into more manageable parts and sends them across a set of machines. The backend system seeks to increase NLP preprocessing efficiency. To show that the backend works, I will demo by distributing jobs to 20 biglab machines. 


This idea originated from my personal need to process large linguistic datasets. For one of my previous projects, I had to Part-of-Speech tag a full year of New York Times Article corpus and that took quite a while. I had to break (manually) the task into 20 jobs and distribute all the tasks across 20 machines. Even with that level of parallelism, the entire job took 2.5 hours! And then, I had to merge (manually) all the results together. 

The distributed job dispatcher can be viewed as a simpler version of Hadoop. The dispatcher has a very generic interface, where it's very easy to specify type of operation to be ran on the specified data. The contribution of this system is twofold. First, Hadoop is a complex system so it requires users to study the documentation to be able to use it but dispatcher is designed so that it's very easy to pick up. Two, python is a good prototype langauge. Having a dispatcher that's native to python means that you can easily test your prototype using the same programming language. Note that the dispatcher should be able to work with any type of tasks and not just NLP-related tasks. The web application is a proof-of-concept of how the paralleism enabled by the dispatcher is helpful for speeding up processing computationally intensive taks. A big part of this project is going to be integrating packages since some NLP libraries are not implemented in python. For example, the stanford entity recognition module is in java. To boost performance, a scheme has to be developed to mix the two (write wrappers).

It's also a great learning opportunity to learn about os-related libraries, server packages, and frontend development in the python ecosystem.

# Goals

- Build a frontend system that enables visitors to submit NLP tasks.
- Support the following NLP tasks from both the fronend and the backend: entity recognition, topic detection, dependency parsing, preprocessing, tokenizing, tagging
- Build a backend system that partitions the task at hand into more manageable pieces and distribute them to other machines (I will be distributing jobs to biglab machies since these machines have unlimited job processing time allowance). The dispatcher should allow worker monitoring, fault tolerance, logging, and job scheduling.
- Make the system into an API

*Note that the I will be using external NLP libraries to run the tasks.

# Packages

## Python Dependencies

- [flask] (http://flask.pocoo.org/)
- [twisted] (http://twistedmatrix.com/trac/) (to support async callbacks)
- [nltk] (http://nltk.org/)
- [scoop] (https://code.google.com/p/scoop/)
- [paramiko] (https://github.com/paramiko/paramiko)

## Non-Python Dependencies

- [Stanford NLP software] (http://nlp.stanford.edu/software/corenlp.shtml)
- [SIMetrix] (http://www.cis.upenn.edu/~lannie/IEval2.html)

