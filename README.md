# Dynamic Read-Quorum Scaling in Cloud Native Storage

Our team "Cloudy Howdy" won the 2nd Runner-up prize at Veritas illuminate U-Connect "Conquer the Cloud" Hackathon 2023. More than 115 teams from 30 colleges participated in this hackathon.

Methodology:

We maintain two quorums in every availability zone- a read quorum and a write quorum
Write quorum:
	This consists of a group of nodes that will participate first-hand in the event of a written request. A written request will proceed to the commit stage only when a master node receives an acknowledgement from all the nodes in the quorum.
Advantage: this way, a written request will not wait for every node’s ack, only for the quorum, engines such as Aurora have experienced huge performance gains with this method

Read Quorum:
	This consists of a group of nodes, that will redistribute all the read requests amongst themselves in the most efficient way, this will provide high availability. The master node will maintain the data regarding the number of requests the node is handling. We have employed graph-based methods, that will redirect the request to the database available in the closest availability zone.

Crux of our solution:

    Dynamic scaling refers to the ability of a system to automatically adjust its resources based on workload. 
In our case, we will freeze some of the nodes in every availability zone, i.e these databases will be in the soft state, and will not receive any updates that are being currently made.
As soon as the master node detects a surge in the traffic of read requests, it will initiate an “unfreeze function” that will use the write-ahead log files and make the node consistent.
This technique allows the system to maintain availability and consistency in the face of changing load conditions.
Moreover, since these nodes will be in the frozen state, we achieve performance gains in the write requests, as fewer nodes will need to be updated at run-time.

This introduces a lambda inspired “you pay only for what you use” system.
This will help to significantly bring down the costs whilst maintaining the same level of availability, reliability and fault tolerance.


