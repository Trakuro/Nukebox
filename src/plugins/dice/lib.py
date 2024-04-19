import re
from abc import ABC, abstractmethod
from enum import Enum
from random import randint


class DiceMode(Enum):
    regular = 1
    keep_highest = 2
    keep_lowest = 3

    @classmethod
    def from_str(cls, text: str) -> "DiceMode":
        match text:
            case "kl":
                return DiceMode.keep_lowest

            case "kh":
                return DiceMode.keep_highest

            case "":
                return DiceMode.regular

            case _:
                raise ValueError("Invalid Dice Mode.")


def roll_dice(number, sides, mode: DiceMode = DiceMode.regular) -> int:
    rolls = [randint(1, sides) for _ in range(number)]

    match mode:
        case DiceMode.regular:
            return sum(rolls)

        case DiceMode.keep_highest:
            return max(rolls)

        case DiceMode.keep_lowest:  # keep_lowest
            return min(rolls)

        case _:
            raise ValueError("Unknown Dice Mode.")


class Expression(ABC):
    @classmethod
    def from_str(cls, expression: str) -> "Expression":
        infix_tokens = re.findall(r"\d*d\d+(?:kh|kl|)|\d+|[-+*/()]", expression)
        stack = []
        postfix_tokens = []

        for token in infix_tokens:
            if token.isdigit() or ("d" in token):
                postfix_tokens.append(token)
            elif token == "(":
                stack.append("(")
            elif token == ")":
                while stack and (stack[-1] != "("):
                    postfix_tokens.append(stack.pop())
                stack.pop()
            elif token in "+-":
                while stack and (stack[-1] in "+-*/"):
                    postfix_tokens.append(stack.pop())
                stack.append(token)
            elif token in "*/":
                while stack and (stack[-1] in "*/"):
                    postfix_tokens.append(stack.pop())
                stack.append(token)
            else:
                raise ValueError("Unsolved parenthesis: {token}")

        while stack:
            postfix_tokens.append(stack.pop())

        for token in postfix_tokens:
            if token.isdigit():
                stack.append(ConstExpression(token))

            elif "d" in token:
                left, right = token.split("d")
                number = int(left) if left else 1
                if "kh" in right:
                    mode = DiceMode.keep_highest
                    sides = int(right.replace("kh", ""))
                elif "kl" in right:
                    mode = DiceMode.keep_lowest
                    sides = int(right.replace("kl", ""))
                else:
                    mode = DiceMode.regular
                    sides = int(right)

                stack.append(DiceExpression(number, sides, mode))

            else:
                match token:
                    case "+":
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(Addition(left, right))
                    case "-":
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(Subtraction(left, right))
                    case "*":
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(Multiplication(left, right))
                    case "/":
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(Division(left, right))

        return stack[0]

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def eval(self) -> int:
        pass


class ConstExpression(Expression):
    def __init__(self, expr) -> None:
        self.expr = expr

    def eval(self) -> int:
        return int(self.expr)


class DiceExpression(Expression):
    def __init__(self, number, sides, mode: DiceMode = DiceMode.regular) -> None:
        self.number = number
        self.sides = sides
        self.mode = mode

    def eval(self) -> int:
        return roll_dice(self.number, self.sides, self.mode)


class Addition(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def eval(self) -> int:
        return self.left.eval() + self.right.eval()


class Subtraction(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def eval(self) -> int:
        return self.left.eval() - self.right.eval()


class Multiplication(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def eval(self) -> int:
        return self.left.eval() * self.right.eval()


class Division(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def eval(self) -> int:
        right_val = self.right.eval()
        if right_val == 0:
            raise ValueError("Division by zero")
        return self.left.eval() // right_val
