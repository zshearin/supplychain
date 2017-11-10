import numpy as np

MAX_LENGTH_CAP_SCHED = 9999
#MAX_LENGTH_JOB = 9999999999
"""
class CapacitySchedule:
	def __init__(self, schedule, jobCompletionTimeList):
		self.schedule = schedule
		self.job = jobCompletionTimeList
		self.finish = MAX_LENGTH_JOB
"""
class TimeSlot:
	def __init__(self,  jobNum, taskNum, taskLen):
		self.job = jobNum
		self.taskNum = taskNum
		self.taskLen = taskLen
		self.assigned = False
		self.slack = 0

	def setSlack(self,slack):
		self.slack = slack


def findEndTimes(capSched):

	endTimes = np.zeros((len(capSched)))

	for i in range(len(capSched)):
		if (capSched[i].taskLen + i + 1 > endTimes[i]):
			endTimes[i] = capSched[i].taskLen

	return endTimes

def editSchedule(capSched,jobNum, taskNum, taskLen):
	time = TimeSlot(jobNum, taskNum, taskLen)
 
	N = len(capSched)
	#oldSched = capSched

	newSched = capSched
	sumLen = 99999999999999999
	
	prevIndex = 0
	addedElement = False

	for i in range(N):

		#insert job into schedule
		capSched.insert(i,time)
		#
		endTimes = findEndTimes(capSched)
		

		sum = 0
		for j in range(len(endTimes)):
			sum = sum + endTimes[j]

		if (sum < sumLen):
			
			if (addedElement):
				newSched.pop(prevIndex)

			addedElement = True
			prevIndex = i
			sumLen = sum
			newSched.insert(i, time)


		capSched.pop(i)

	return newSched


def scheduler(jobs):
	
	capSched = []
	for i in range(len(jobs[0])):
		time = TimeSlot(1, i+1,jobs[0][i])
		capSched.append(time)

	for i in range(len(jobs)):

		for j in range(len(jobs[i])):

			if (i == 0):
				break

			capSched = editSchedule(capSched, i+1, j+1, jobs[i][j])
			"""
			for i in range(len(capSched)):
				cur = i + 1
				if (capSched[i] != None):
					print( "t=" + str(cur) + "  |   "+ str(capSched[i].job) + "  |  " + str(capSched[i].taskNum) + "   |   "  + str(capSched[i].taskLen))
			"""




	return capSched
	

if __name__ == "__main__":


	job = [10,8,6,4,2]

	jobs = []
	jobs.append(job)
	jobs.append(job)
	jobs.append(job)
	#jobs.append(job)
	#jobs.append(job)

	capacity = scheduler(jobs)


	print("Time |  Job | Task | Length")

	
	for i in range(len(capacity)):
		cur = i + 1
		if (capacity[i] != None):
			print( "t=" + str(cur) + "  |   "+ str(capacity[i].job) + "  |  " + str(capacity[i].taskNum) + "   |   "  + str(capacity[i].taskLen))
	

