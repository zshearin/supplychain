
from scheduler import *
import random 
import sys

def scheduleListOfJobs(jobs):
	numberOfJobs = len(jobs)
	
	#create empty capacity schedule
	CapacitySched = []
	for i in range(MAX_LEN_CAP_SCHEDULE):
		timeSlot = TimeSlot()
		CapacitySched.append(timeSlot)

	#Assign initial job (first vector within vector)
	CapacitySched = assignInitialJob(CapacitySched,jobs)

	#Assign all other jobs (2nd to nth jobs where n is number of jobs)
	CapacitySched = assignRestOfJobs(CapacitySched, jobs)


	#shift back any jobs that have empty time slots before them
	shiftBack(CapacitySched)

	curSumOfEndTimes = getSumOfEndTimes(numberOfJobs, CapacitySched)
	
	modifySchedule = CapacitySched.copy()


	adjustmentsToCapSched = 0
	while(True):

		dictList = createSlackDictionary(modifySchedule, numberOfJobs)

		newSchedule = readjustCapacitySchedule(modifySchedule, dictList)

		newSumOfEndTimes = getSumOfEndTimes(numberOfJobs, newSchedule)

		if (newSumOfEndTimes == curSumOfEndTimes):
			break
		
		adjustmentsToCapSched = adjustmentsToCapSched + 1

		curSumOfEndTimes = newSumOfEndTimes
		modifySchedule = newSchedule.copy()

	return CapacitySched, newSchedule, adjustmentsToCapSched
	
#create a function to print the schedules
#(if there's any difference, print old and new)
#(if no difference only print one)
def printCapacitySchedules(oldSched, newSched, numberOfJobs):
	different = False
	for i in range(len(oldSched)):
		if (oldSched[i].assigned == False):
			continue
		old = oldSched[i].task
		new = newSched[i].task
		if not (old.getJobNum() == new.getJobNum() and old.getTaskLen() == new.getTaskLen()):
			different = True
	print("="*50)
	if (different):
	#Print out old schedule and new schedule (if no adjustments, old schedule should be the same as new schedule)
		print("Old Schedule:")
		printSlackValues(oldSched)
		print("="*50)
		printEndTimes(numberOfJobs, oldSched)
		print("="*50)
		print("="*50)
		
		print("New Schedule:")
		printSlackValues(newSched)
		print("="*50)
		printEndTimes(numberOfJobs, newSched)
		#print("not implemented yet")
	else:
		print("Schedule: ")
		printSlackValues(newSched)
		print("="*50)
		printEndTimes(numberOfJobs, newSched)

if __name__ == "__main__":


	
	numberOfJobs = 25
	nummberOfPathTasks = 3
	minPathLength = 4
	maxPathLength = 13

	jobs = []
#	"""
	for i in range(numberOfJobs):
		curJob = []
		for j in range(nummberOfPathTasks):
			curTask = random.randint(minPathLength, maxPathLength)
			curJob.append(curTask)
		curJob.sort(reverse=True)
		jobs.append(curJob)

	
	for i in range(len(jobs)):
		print("Job " + str(i+1))
		for j in range(len(jobs[i])):
			print(str(jobs[i][j]) + " ", end='')
		print("\n")
#	"""



	oldSchedule, newSchedule, numberOfAdjustments = scheduleListOfJobs(jobs)

	printCapacitySchedules(oldSchedule, newSchedule, numberOfJobs)
	print("="*50)
	print("Number of Adjustments: " + str(numberOfAdjustments))