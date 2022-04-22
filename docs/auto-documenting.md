# Why Auto Document

Documentation is important, architecture diagrams especially so. Architecture diagrams can be used for many reasons such as.
- Illustrating problems
- Proposing a solution
- Auditing a system
- Approval of current state and new state.
- Explaining a system

The more parts in a system the more a diagram tends to be required. 

You can create pages of written documentation but 
people are inherently visual creatures.  A visual representation of something is easier to talk over with a bussiness owner or project team than a textual one, and the users might see patterns or problems in the solution which were not seen by technical teams.

## Why is this a problem in the cloud

In the cloud there is a trend to move towards microservices or serverless systems.  These systems share many traits with enterprise messaging systems of the past with many moving parts held together by configuration.  When we have these many moving parts it becomes hard to hold all this complexity in your head at a time, and harder still to explain it.  So you make diagrams.

## Problem with Manual Documentation
Diagrams start reflecting the ideal of what should be built and may even match the initial implementation.  Even with 'living' documentation it takes considerable time and effort to keep this current.  Over time due to pressures in development diagrams tend to get out of date.

An out of date diagram can misinform people and can lead to bad decisions being made.  This could be budgetary or it could be operational.  A bad backup document could lead to lost data or a bad architecture diagram could lead of important systems being removed.

## Auto Documentation
Auto documentation is the idea that you will generate diagrams from reality automatically.  The most common example of this might be AWS xray service maps or an nmap diagram or a route map on google.  In the cloud architecture world 

The diagrams created could be used as a basis of future proposals so the starting view is accurate.  

Another use is to make this part of a CI/CD process which would auto document a software release allowing users to have accurate documentation for when problems occcur or to allow non technical product owners to review changes between releases.  The automation makes these uses trivial for the tech teams to support while giving more information in an easy to consume format to the users.


## How does Surveyor help

The idea of this project is to create standardised diagrams of various types for use in ci/cd pipelines (scheduled or change triggerred) based on the infrastructure that has already been deployed.  By being based on the infrastructure it should always reflect reality.



