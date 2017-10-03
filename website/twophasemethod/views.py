from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, QueryDict
from pprint import pprint
from fractions import *
from decimal import *

# Create your views here.
def twoPhaseMethod(inputMatrix):
    def minimumRowRatioIndex(matrix, columnIndex):
        ratioList = []
        for i in range(len(constraints)):
            if matrix[i][columnIndex] > 0:
                # print(matrix[i][-1], '/', matrix[i][columnIndex])
                rowRatio = matrix[i][-1] / matrix[i][columnIndex]
                ratioList.append(rowRatio)
            else:
                ratioList.append(Fraction('999'))
        print(ratioList)
        return ratioList.index(min(ratioList))

    def setIdentityColumn(rowPivot, columnPivot):
        if matrix[rowPivot][columnPivot] != 1:
            baseDivider = matrix[rowPivot][columnPivot]
            for i in range(len(matrix[rowPivot])):
                # print(matrix[rowPivot][i], '/dfdsf', matrix[rowPivot][columnPivot], rowPivot, columnPivot)
                matrix[rowPivot][i] /= baseDivider

        for i in range(len(matrix)):
            if i == rowPivot or matrix[i][columnPivot] == 0:
                continue
            baseMultiplier = abs(matrix[i][columnPivot])
            if matrix[i][columnPivot] > 0:
                for j in range(len(matrix[i])):
                    matrix[i][j] -= baseMultiplier*matrix[rowPivot][j]
            else:
                for j in range(len(matrix[i])):
                    matrix[i][j] += baseMultiplier*matrix[rowPivot][j]
        solutionSet[rowPivot] = columnPivot

    # decomposition of matrix components
    objectiveFunc = inputMatrix[0]
    constraints = inputMatrix[1:]
    constants = []
    numOfArtificial = len(constraints)
    negativeConstraints = []
    pprint(inputMatrix)

    # identify the needed number of artificial variables to be added
    for j in range(len(inputMatrix[0]) - 1):
        rowPivot = 0
        numOfZeroes = 0
        numOfOnes = 0
        for i in range(len(inputMatrix)):
            if inputMatrix[i][j] == '0':
                numOfZeroes += 1
            elif inputMatrix[i][j] == '1' or inputMatrix[i][j] == '-1':
                numOfOnes += 1
                rowPivot = i
            else:
                continue
        if (numOfZeroes == len(inputMatrix)-1 and numOfOnes == 1 and
          ((int(inputMatrix[rowPivot][j]) == 1 and int(inputMatrix[rowPivot][-1]) > 0) or
           (int(inputMatrix[rowPivot][j]) == -1 and int(inputMatrix[rowPivot][-1]) < 0))
        ):
            numOfArtificial -= 1
            if int(inputMatrix[rowPivot][j]) == -1 and int(inputMatrix[rowPivot][-1]) < 0:
                negativeConstraints.append(rowPivot-1)  # the arrangement of the initial matrix is different and requires a minus one

    print("Artific", numOfArtificial)
    for i in range(len(inputMatrix)):
        constants.append(inputMatrix[i][-1])
        inputMatrix[i].pop()
    numOfVars = len(constraints[0])

    # prepare the matrix with artificial variables
    objectiveFuncArt = ['0' for i in range(len(objectiveFunc))]
    objectiveFunc.extend(['0' for i in range(numOfArtificial)])
    objectiveFunc.append(constants[0])
    objectiveFuncArt.extend(['1' for i in range(numOfArtificial)])
    objectiveFuncArt.extend('0')

    identityMatrix = [['0' for i in range(len(constraints))] for j in range(len(constraints))]
    for i in range(len(constraints)):
        identityMatrix[i][i] = 1
        constraints[i].extend(identityMatrix[i][:numOfArtificial])
        constraints[i].append(constants[i+1])

    # establish the new extended matrix
    matrix = []
    for i in range(len(constraints)):
        matrix.append(constraints[i])
    matrix.append(objectiveFunc)
    matrix.append(objectiveFuncArt)
    solutionSet = [-1 for i in range(numOfVars)]

    print(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = Fraction(matrix[i][j])
    for row in negativeConstraints:
        for i in range(len(matrix[row])):
            matrix[row][i] *= -1

    # re-assign variables that are referenced to the new matrix
    objectiveFunc = matrix[-2]
    objectiveFuncArt = matrix[-1]
    for i in range(len(matrix) - 2):
        constraints[i] = matrix[i]

    for i in range(len(matrix)):
        print(matrix[i])
    print('\n')

    # Phase I: zeroed out artificial objective function
    ctr = 0
    for i in range(numOfArtificial):
        # print("GO", matrix[i], matrix[i][numOfVars+ctr], numOfVars+ctr)
        setIdentityColumn(rowPivot=i, columnPivot=numOfVars+ctr)
        ctr += 1
    for i in range(len(matrix)):
        print(matrix[i])
    print('\nStart of PHASE I')

    for i in range(numOfVars):
        print("objFunc", objectiveFuncArt[i])
        if objectiveFuncArt[i] < 0:
            rowPivot = minimumRowRatioIndex(matrix=matrix, columnIndex=i)
            print("identityPivot", (rowPivot, i), matrix[rowPivot][i])
            setIdentityColumn(rowPivot=rowPivot, columnPivot=i)
        for i in range(len(matrix)):
            print(matrix[i])

    print('\nStart of PHASE II')
    # Phase II: simplex algorithm
    for i in range(numOfVars):
        if objectiveFunc[i] < 0:
            rowPivot = minimumRowRatioIndex(matrix=matrix, columnIndex=i)
            print("identityPivot", (rowPivot, i), matrix[rowPivot][i])
            setIdentityColumn(rowPivot=rowPivot, columnPivot=i)
        for i in range(len(matrix)):
            print(matrix[i])
        print('\n')

    formatMatrix = []
    solutionValue = objectiveFunc[-1] * -1
    solutionValue = str(solutionValue.numerator) + ("" if solutionValue.denominator == 1 else "/" + str(solutionValue.denominator))
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            denominatorStr = "" if matrix[i][j].denominator == 1 else ('/' + str(matrix[i][j].denominator))
            row.append(str(matrix[i][j].numerator) + denominatorStr)
        formatMatrix.append(row)

    print(numOfVars, solutionSet)
    finalSolutionSet = ["0" for i in range(numOfVars)]
    for i in range(len(solutionSet)):
        if solutionSet[i] < numOfVars:
            finalSolutionSet[solutionSet[i]] = formatMatrix[i][-1]

    return {"solutionValue": solutionValue, "solutionSet": finalSolutionSet, "matrix": formatMatrix}

def index(request):
    template = "index.html"
    return render(request, template)

def compute_solution(request):
    inputMatrix = request.GET["matrix"]
    inputMatrix = eval(inputMatrix)
    outputMatrix = twoPhaseMethod(inputMatrix)
    return JsonResponse({"outputMatrix": outputMatrix})
