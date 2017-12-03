
class Time:

	def __init__(self, jobNum, taskLen, slack):
		self.jobNum = jobNum
		self.taskLen = taskLen
		self.slack = slack


	def getSlack(self):
		return self.slack
	def setSlack(self, slack):
		self.slack = slack

	def getJobNum(self):
		return self.jobNum

	def getTaskLen(self):
		return self.taskLen


#input: the job endtime, job number and capacity schedule
# takes any jobs with same job number ans job end time and readjusts based on new job end time
def changeSlackTimes(jobEndTime, jobNumber, CapacitySchedule):
	
	for i in range(len(CapacitySchedule)):

		if (CapacitySchedule[i].jobNum == jobNumber):
			currentTaskEndTime = CapacitySchedule[i].taskLen + i 
			slack = jobEndTime - currentTaskEndTime

			CapacitySchedule[i].setSlack(slack)

#input: LIST OF TASKS (A SINGLE JOB)
#return: the endtime for that job, and an initialized capacity schedule
def assignInitialJob(job):
	#print("not implemented yet")

	CapacitySchedule = []

	EndTime = job[0]

	curSlack = 0
	for i in range(len(job)):

		#if the new task adds to the end time, reset end time and change all tasks' slack times
		if (job[i] + i > EndTime):
			#change end time
			EndTime = job[i] + i

			#call function to readjust slack times
			changeSlackTimes(EndTime, 1, CapacitySchedule)

			#ALSO NEED TO REASSIGN THE REST OF THE END TIMES FOR THE JOBS 

		#CALCULATE SLACK
		curSlack = EndTime - job[i] - i

		#CREATE OBJECT TO ADD TO CAPACITY SCHEDULE
		capAssignment = Time(1,job[i],curSlack)

		#add to capacity schedule (assuming task lengths are in order)
		CapacitySchedule.append(capAssignment)

	return EndTime, CapacitySchedule


def getJobEndTime(jobNum, CapacitySchedule):

	maximum = 0
	for i in range(len(CapacitySchedule)):

		if (CapacitySchedule[i].jobNum == jobNum):

			if (CapacitySchedule[i].taskLen + i > maximum):
				maximum = CapacitySchedule[i].taskLen + i
				

	return maximum


def increaseSlackForJob(jobNum, CapacitySchedule):
	#print("not yet implemented yet")

	for i in range(len(CapacitySchedule)):
		if (CapacitySchedule[i].getJobNum() == jobNum):

			currentSlack = CapacitySchedule[i].getSlack()
			CapacitySchedule[i].setSlack(currentSlack + 1)



#find the right spot to add the task 
#return the index
def findTaskSpot(jobNum, taskLen, CapacitySchedule):

	
	oldSched = CapacitySchedule.copy()
	minIndex = len(CapacitySchedule)


	##################################################################
	##############  TRY FIRST JOB SPOT BY APPENDING TO THE END #######
	time = Time(jobNum,taskLen,0)
	CapacitySchedule.append(time)

	EndTimes = []
	curEndTime = 0
	for j in range(jobNum):

		curEndTime = getJobEndTime(j+1, CapacitySchedule)
		EndTimes.append(curEndTime)


	for j in range(jobNum):
	
		# I need an end Time vector calculation 
		changeSlackTimes(EndTimes[j], j, CapacitySchedule)

		for k in range(len(CapacitySchedule)):

			while(CapacitySchedule[k].getSlack() < 0):
				curJobNum = CapacitySchedule[k].getJobNum()

				increaseSlackForJob(curJobNum, CapacitySchedule)
	minSum = 0
	for j in range(len(EndTimes)):
		minSum = minSum + EndTimes[j]


	CapacitySchedule = oldSched.copy()

	##################################################################

	##################################################################
	############## 		TRY ALL OTHER SPOTS ##########################

	for i in reversed(range(len(CapacitySchedule))):
#	for i in range(len(CapacitySchedule)):

		time = Time(jobNum, taskLen, 0)
		
		#insert time object into index i
		CapacitySchedule.insert(i, time)

		#printSlackValues(CapacitySchedule)
		#add to Capacity Schedule

		EndTimes = []
		curEndTime = 0
		for j in range(jobNum):

			curEndTime = getJobEndTime(j+1, CapacitySchedule)
			EndTimes.append(curEndTime)


		for j in range(jobNum):
	
			# I need an end Time vector calculation 
			changeSlackTimes(EndTimes[j], j, CapacitySchedule)

			for k in range(len(CapacitySchedule)):

				while(CapacitySchedule[k].getSlack() < 0):
					curJobNum = CapacitySchedule[k].getJobNum()

					increaseSlackForJob(curJobNum, CapacitySchedule)


		curSum = 0

		for j in range(len(EndTimes)):
			curSum = curSum + EndTimes[j]

		if (curSum < minSum):
			minSum = curSum
			minIndex = i

		"""
		print("adjusted slack times: ")
		printSlackValues(CapacitySchedule)

		print("="*40)
		print("Sum of end times: " + str(curSum))
		print("="*40)
		"""

		CapacitySchedule = []
		for k in range(len(oldSched)):
			CapacitySchedule.append(oldSched[k])


		CapacitySchedule = oldSched.copy()

#	print(minIndex)
	return minIndex, oldSched



#add the task to the index

def addTaskToIndex(index, jobNum, taskLen, CapacitySchedule):

	time = Time(jobNum, taskLen, 0)
	
	#add Time object to capacity schedule
	if (index == len(CapacitySchedule)):
		CapacitySchedule.append(time)
	else:
		CapacitySchedule.insert(index,time)

	#adjust slack times based on addition

	MaxJob = 0
	#get the total number of jobs that exist in the capacity schedule
	for i in range(len(CapacitySchedule)):
		if (CapacitySchedule[i].getJobNum() > MaxJob):
			MaxJob = CapacitySchedule[i].getJobNum()

	#calculate each job end time in the capacity schedule
	EndTimes = []
	curEndTime = 0
	for i in range(MaxJob):
	#def getJobEndTime(jobNum, CapacitySchedule):
		curEndTime = getJobEndTime(i+1, CapacitySchedule)
		EndTimes.append(curEndTime)



	#adjust slack times based on end times vector
	for i in range(MaxJob):
		#def changeSlackTimes(jobEndTime, jobNumber, CapacitySchedule):
		changeSlackTimes(EndTimes[i], i+1, CapacitySchedule)

	#printSlackValues(CapacitySchedule)
	#print("="*50)



def assignAllJobs(jobList):
	
	intialEndTime = 0
	CapSched = []

	EndTimes = []

	initialEndTime, CapSched = assignInitialJob(jobList[0])
	EndTimes.append(initialEndTime)

	oldSched = CapSched.copy()

	#add all jobs in the job list:
	for i in range(len(jobList)):
		
		#if it is the initial job, don't do anything (already initialized)
		if (i == 0):
			continue
		
		#add all tasks in an individual job		
		for j in range(len(jobList[i])):
			
			newSched = []
			jobNum = i + 1
			taskLen = jobList[i][j]
	
			#find what index is best place to put job
			index, newSched = findTaskSpot(jobNum, taskLen, oldSched)
			
			#place job at optimal location found
			addTaskToIndex(index, jobNum, taskLen, newSched)
	
			oldSched = newSched.copy()

	return newSched


#display the information regarding the created capacity schedule
def printSlackValues(CapacitySchedule):
	print()
	for i in range(len(CapacitySchedule)):

		print("t=" + str(i) + ": job num: " + str(CapacitySchedule[i].jobNum) + ", task len: " + str(CapacitySchedule[i].taskLen) +  ", slack: " + str(CapacitySchedule[i].slack))

#Iterate through the EndTimes vector and print out values with the job numbers
def printEndTimes(EndTimes):

	print("End Times:")
	for i in range(len(EndTimes)):
		print("Job " + str(i+1) +": " + str(EndTimes[i]))

if __name__ == "__main__":


	job = [10,9,9,7,5]
	#job2 = [10,8,6,4,2]
	#job3 = [10,8,6,4,2]

	jobs = []
	for i in range(3):
		jobs.append(job)
	


	capacity = assignAllJobs(jobs)

	printSlackValues(capacity)

	numberOfJobs = len(jobs)

	EndTimes = []
	print("End Times: ")
	for i in range(numberOfJobs):

		curEndTime = getJobEndTime(i+1, capacity)
		print("Job " + str(i+1) + ": " + str(curEndTime))
		EndTimes.append(curEndTime)

