from pair import nil, Pair
from operator import add, sub, mul, truediv

def tokenize(expression):
    expression = expression.replace('(', ' ( ').replace(')', ' ) ')
    tokens = expression.split()
    return tokens
def parse(tokens):
    def parse_tokens(tokens, index):
        if index >= len(tokens):
            raise SyntaxError

        token = tokens[index]

        if token == '(':
            operator = tokens[index + 1]
            if index != 0:
                # This is a sub-expression
                sub_expr, new_index = parse_tokens(tokens, index + 2)
                first = Pair(operator, sub_expr)
                index = new_index
            else:
                first = operator
                index += 2

            rest, new_index = parse_tokens(tokens, index)
            return Pair(first, rest), new_index

        elif token == ')':
            # End of current Pair list
            return nil, index + 1

        else:
            # This should be an operand
            try:
                if '.' in token:
                    value = float(token)
                else:
                    value = int(token)
            except ValueError:
                raise TypeError

            rest, new_index = parse_tokens(tokens, index + 1)
            return Pair(value, rest), new_index

    parsed, _ = parse_tokens(tokens, 0)
    return parsed

def reduce(func, operands, initial) -> int:
    result = initial
    current = operands
    while current is not nil:
        result = func(result, current.first)
        current = current.rest
    return result

def apply(operator, operands):
    if operator == '+':
        return reduce(add, operands, 0)
    elif operator == '-':
        return reduce(sub, operands.rest, operands.first)
    elif operator == '*':
        return reduce(mul, operands, 1)
    elif operator == '/':
        return reduce(truediv, operands.rest, operands.first)
    raise TypeError

def eval(exp):
    if isinstance(exp, (int, float)):
        return exp
    if isinstance(exp, Pair):
        #subexpression!!
        operator = exp.first
        operands = exp.rest.map(eval)
        return apply(operator, operands)
    raise TypeError

def main_loop():
    prompt = input("calc >> ")
    if prompt == "exit":
        return "exit"
    else:
        tokens = tokenize(prompt)
        try:
            result = parse(tokens)
            evaluation = eval(result)
        except ValueError:
            print(ValueError)
            return
        except TypeError:
            print(TypeError)
            return
        except SyntaxError:
            print(SyntaxError)
            return

        ###IDK step 4,5,6 of the main loop here, parsing and validation
        print(evaluation)
        return

def main():
    print("Welcome to the CS 111 Calculator Interpreter.")
    #main loop should follow the greeting
    while main_loop() != "exit":
        pass
    print("Goodbye!")

if __name__ == "__main__":
    main()
