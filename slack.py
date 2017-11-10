import numpy as np

MAX_LENGTH_CAP_SCHED = 5000

class TimeSlot:
	def __init__(self,  jobNum, taskNum):
		self.job = jobNum
		self.task = taskNum
		self.assigned = False
		self.slack = 0

	def setSlack(self,slack):
		self.slack = slack

def editSchedule(Capacity,jobNum,taskLen):
	print("NOT IMPLEMENTED YET")

	#check each spot that the task could be added 

		#for an individual add: 
			#add 1 to the total end time 
			#pick spot to add job
			#shift all jobs right one that are at or after 
			#add one to slack for items before the job

			#assess job completion time (for each job)
			#assess total completion time (for all jobs)

	#for all the jobs permutations assessed 

	#check all ways to add the task

	#determine which method minimizes a certain aspect 



		#whichever one minimizes the day to completion, choose it 



def scheduler(jobs):
	
	#create the capacity schedule (an array of TimeSlot objects)
	Capacity = []
	for i in range(MAX_LENGTH_CAP_SCHED):
		Capacity.append(None)

	endTime = 0
	#Iterate through the 2D array of Jobs and tasks:
	#jobs[i][j] - jth task of the ith job
	for i in range(len(jobs)):

		#for each task in the individual job list
		for j in range(len(jobs[i])):
			curLen = jobs[i][j]

			#place first job
			if (i == 0 and j == 0):
				endTime = curLen
				t = TimeSlot(i+1,j+1)
				Capacity[0] = t
				continue

			#check spot where there would be no slack (optimal placement)
			if (Capacity[endTime-curLen] == None):
				t = TimeSlot(i+1, j+1)
				t.assigned = True
				Capacity[endTime-curLen] = t
			

			#CREATE AND ELIF THAT ASSESSES IF (job[i][j] == Capacity[endTime-curLen])

				#if it does, 


			#iterate back to see if open spot for the job 
			#(keeping track of the slack) 
			else:
				added = False
				curSpot = endTime-curLen - 1
				slack = 0
				while(True):
					slack = slack + 1
					if (curSpot < 0):
						break

					#
					if (Capacity[curSpot] == None):

						##if the one ahead of it has same


						t = TimeSlot(i+1,j+1)
						t.assigned = True
						t.setSlack(slack)
						Capacity[curSpot] = t
						added = True
						break

					curSpot = curSpot - 1

				#make assessment for adjustment to entire capacity scheduling
				if (added == False):
					editSchedule(Capacity,i+1, jobs[i][j])

					#call a function to make the slack assessment
					#print("havent implemented add if all spots inside taken")

				#find a spot for the job
				#iterate through the previous potential time slots to find open one
					#if open one found, place and move on 
					#if open one not found, add to the end of the list

	#add the rest of the jobs to the schedule
	return Capacity


def scheduler2(jobs):
	print("havent implemented either")
	#add the job to the first available slot, record the slack

	#implement another function to assess slack values and insert appropriately
		#dynamic 



#try another implementation: start with 

if __name__ == "__main__":


	job = [10,8,6,4,2]

	jobs = []
	jobs.append(job)
	jobs.append(job)
	jobs.append(job)

	capacity = scheduler(jobs)


	print("Time |  Job | Task")
	for i in range(len(capacity)):
		cur = i + 1
		if (capacity[i] != None):
			print( "t=" + str(cur) + "  |   "+ str(capacity[i].job) + "  |  " + str(capacity[i].task))
	