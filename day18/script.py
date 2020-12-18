import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re
from enum import Enum

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

class OPERATOR(Enum):
    SUM = '+'
    PRODUCT = '*'

OPERATORS = [OPERATOR.SUM.value, OPERATOR.PRODUCT.value]

# Regex to do smallest parenthesis sub expression first
SUB_EXPRESSION_REGEX = re.compile(r'(\([^()]*?\))')

# Evaluate sub expression without parenthesis
def evaluateSubExpression(expression: str, precedenceOperator: OPERATOR = None) -> int:
    while True:
        expressionMembers = expression.split(' ')
        precedenceOperatorIndex = None
        if precedenceOperator is not None:
            precedenceOperatorIndex = next((i for i, x in enumerate(expressionMembers) if x == precedenceOperator.value), None)

        if precedenceOperatorIndex is not None:
            # Evaluating operator with precedence first
            leftMostExpressionMembers = expressionMembers[precedenceOperatorIndex - 1 : precedenceOperatorIndex + 2]
        else:
            leftMostExpressionMembers = expressionMembers[:3]
            if len(leftMostExpressionMembers) == 1:
                break # No more operators

        # Evaluating leftmost expression
        (leftValue, operator, rightValue) = (int(leftMostExpressionMembers[0]), OPERATOR(leftMostExpressionMembers[1]), int(leftMostExpressionMembers[2]))
        result = leftValue + rightValue if operator == OPERATOR.SUM else leftValue * rightValue

        # Substituing result in expression
        expression = expression.replace(' '.join(leftMostExpressionMembers), str(result), 1)

    leftMostExpressionMembers = expression.split(' ')[:3]

    return int(expression) # All that remains is answer value

def evaluateExpression(expression: str, precedenceOperator: OPERATOR = None) -> int:
    # Evaluating all sub expressions first
    while True:
        subExpressions = SUB_EXPRESSION_REGEX.findall(expression)
        if len(subExpressions) == 0:
            break # No more parenthesis

        for subExp in subExpressions:
            # Evaluating sub expression
            result = evaluateSubExpression(subExp.replace('(', '').replace(')', ''), precedenceOperator)
            # Substituing result in expression
            expression = expression.replace(subExp, str(result), 1)

    # Evaluating remaining expression from left to right
    return evaluateSubExpression(expression, precedenceOperator)

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
expressions = utils.readFileLines(filename)

########
# PART 1
########

results = [evaluateExpression(e, precedenceOperator=None) for e in expressions]
print('1) Sum of each result values with both SUM and PRODUCT having same precedence = %d' % sum(results))

########
# PART 2
########

results2 = [evaluateExpression(e, precedenceOperator=OPERATOR.SUM) for e in expressions]
print('2) Sum of each result values with SUM having precedence over PRODUCT = %d' % sum(results2))

########
# PART 3
########

results2 = [evaluateExpression(e, precedenceOperator=OPERATOR.PRODUCT) for e in expressions]
print('3) Sum of each result values with PRODUCT having precedence over SUM = %d' % sum(results2))