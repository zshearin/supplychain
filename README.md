# supplychain
Writing code to understand how to optimize reconstruction of disrupted supply chain

When all components of a supply chain are functional, delivery scheduling of supplies can be assumed optimal. In normal operation, however, connections are lost and the delivering order of these supplies must be altered.  The goal of this program is to facilitate research to address how supply chains recover once a path is no longer functional.  The optimizing objectives that have already been considered include minimizing maximum tardiness and minimizing the completion time of the last tardy job.  The objective that this program attempts to tackle is minimizing the total tardiness and include job number in prioritization.

There are four variables that need to be changed in the main.py file based on what conditions want to be observed (primarily to capture influences of tier supplier on min/max path length).  The variables are listed below and can be found in the first four lines of the program:

numberOfJobs (determined by how many suppliers at that tier)
numberOfPathTasks (tasks paths from each supplier)
minPathLength
maxPathLength 

