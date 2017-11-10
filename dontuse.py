import numpy as np


class Job:
	
	#tasks is a list of Task objects
	def __init__(self, tasks, jobNum):
		self.tasks = tasks
		self.jobNum = jobNum

class Task:
	def __init__(self, timeForCompletion):
		self.t = timeForCompletion



class TimeSlot:
	def __init__(self, timeSlot, taskNum, jobNum):
		self.time = timeSlot
		self.task = taskNum
		self.job = jobNum
		self.assigned = False

#input: list of jobs and Empty Capacity schedule 
	#capacity schedule has a list of TimeSlot objects with assigned == False

#output: filled out capacity schedule
def scheduler(CapSched,Jobs):
	#print("\"scheduler\" not implemented yet")
	#scehdule first jobs

	#keep track of when the job would finish 
	#(eg: schedule task that takes 10 at time 1 and one that takes 7 at time 2, job would finish at 11 (10+1=11)) 

	#1 schedule first job at t = 1
	#2 schedule second job at latest time to not increase overall time taken
		#if it does increase the time (example schedule a task that takes 7 at 1 and you have another 7 task - have to schedule at 2)
		#place in timeslot that minimizes added time for completion
	#3 repeat step 2 for the rest of the jobs in the set of tasks required
	endTime = Jobs[0][0]

	Job1 = TimeSlot(0,1,1)
	Job1.assigned = True

	
	CapSched[0] = Job1
	
	first = True
	counter = 0
	for task in Jobs[0]:
		if (counter == 0):
			counter = counter +1
			continue
		
		if (task < endTime):
			if (CapSched[endTime-task].assigned == False):
				time = TimeSlot(endTime-task, counter, 1)
				time.assigned = True

				CapSched[endTime - task] = time


		#check if task is less than the total current completion time
			#if it is -
				#check if CapSched[endTime-Task] == 0
					#if it is, CapSched[endTime - Task] = TimeSlot( endTime - Task, counter, 1)



		counter = counter +1


	return CapSched

	#after first task set, add the next job to the capicity schedule with the criteria 


	
"""
def sortJobs(Jobs):
	
	for job in Jobs:
		for task in job:
			#sort tasks in job
			print("this is where they're sorted")

	print("\"sortJobs\" not implemented yet")
"""

if __name__ == "__main__":

	t = 40
	#C = np.zeros((t))
	#print(C)

	#J = [10, 8, 7, 6, 5, 5, 3, 2, 2, 1]
	J = [10,8,6,4,2]
	#J = [10,9,8,7,6]
	"""
	sum = 0
	for i in range(len(J)):
		sum = sum + J[i]

	print(sum)
	"""

	Jobs = []
	Capacity = []
	for i in range(t):
		Capacity.append(TimeSlot(0,0,0))

	Jobs.append(J)
	#Jobs.append(J)
	#Jobs.append(J)


	Capacity = scheduler(Capacity, Jobs)

	for timeSlot in Capacity:
		print(timeSlot.assigned)
	
	#print(Capacity)