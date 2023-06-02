#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    elif index < len(line) and line[index] == '(':
        index += 1
        decimal = 0.1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

def read_left_bracket(line, index):
    token = {'type': 'LEFT_BRACKET'}
    return token, index + 1

def read_right_bracket(line, index):
    token = {'type': 'RIGHT_BRACKET'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '(':
            (token, index) = read_left_bracket(line, index)
        elif line[index] == ')':
            (token, index) = read_right_bracket(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFT_BRACKET':
            bracket_count = 1
            for i in range(index+1, len(tokens)):
                if tokens[i]['type'] == 'LEFT_BRACKET':
                    bracket_count += 1
                elif tokens[i]['type'] == 'RIGHT_BRACKET':
                    bracket_count -= 1
                if bracket_count == 0:
                    sub_answer = evaluate(tokens[index+1:i])
                    tokens = tokens[:index] + [{'type': 'NUMBER', 'number': sub_answer}] + tokens[i+1:]
                    return evaluate(tokens)
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLICATION':
                answer *= tokens[index]['number']
            elif tokens[index - 1]['type'] == 'DIVISION':
                answer /= tokens[index]['number']
            elif tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("0")
    test("3*4/2")
    test("3/2/2/19")
    print("==== Test finished! ====\n")
#==== Test started! ====
# PASS! (1+2 = 3.000000)
# PASS! (1.0+2.1-3 = 0.100000)
# PASS! (0 = 0.000000)
# PASS! (3*4/2 = 6.000000)
# PASS! (3/2/2/19 = 0.039474)
# ==== Test finished! ====



run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)