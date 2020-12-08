import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# FETCH DATA
###########################
lineGroups = utils.readFileLineGroups(filename)

########
# PART 1
########

groupAnswers = [''.join(g) for g in lineGroups]
nbUniqueGroupAnswers = [len(set(a)) for a in groupAnswers]
print('1) Sum of group anyone "yes" answers count: %d' % sum(nbUniqueGroupAnswers))

########
# PART 2
########

nbGroups = len(lineGroups)
uniqueGroupAnswers = [set(a) for a in groupAnswers]
groupAnswerCounts = [[groupAnswers[i].count(a) for a in uniqueGroupAnswers[i]] for i in range(nbGroups)]
nbCommonGroupAnswers = [len([count for count in groupAnswerCounts[i] if count == len(lineGroups[i])]) for i in range(nbGroups)]

print('2) Sum of group everyone "yes" answers count: %d' % sum(nbCommonGroupAnswers))