import random
import re
from fractions import Fraction

space = ' '
num = 0  # 记录题目生成个数


def create_fraction(maxnum):
    maxnum = int(maxnum)
    denominator = random.randint(1, maxnum)
    numerator = random.randint(0, maxnum)
    if numerator % denominator == 0:
        return str(int(numerator / denominator))
    elif numerator > denominator:
        integer = int(numerator / denominator)
        numerator -= (denominator * integer)
        return str(integer) + "'" + str(numerator) + "/" + str(denominator)
    return str(numerator) + "/" + str(denominator)


def Digit(count, maxnum):  # count为算式个数
    digit = []
    for i in range(count):
        flag = random.randint(0, 1)  # 0为整数，1为分数
        if flag == 0:
            digit.append(str(random.randint(0, maxnum)))
        else:
            digit.append(create_fraction(maxnum))
    return digit


def Operator(count):
    operator = ['+', '-', '×', '÷']
    saveop = []
    for i in range(count - 1):
        saveop.append(random.choice(operator))
    return saveop


# 无括号
def noBracketFormula(count, maxnum):
    digit = Digit(count, maxnum)
    op = Operator(count)
    formula = digit[0] + space
    for i in range(1, count):
        formula += op[i - 1] + space + digit[i] + space
    formula = formula[:-1]
    return formula


# 一个括号
def oneBracketFormula(count, maxnum):
    digit = Digit(count, maxnum)
    op = Operator(count)
    left = random.randint(0, count - 2)
    right = random.randint(left + 1, count - 1)
    formula = ""
    if left == 0:
        formula = '(' + space + digit[0] + space
    else:
        formula = digit[0] + space
    for i in range(1, count):
        if i == left:
            formula += op[i - 1] + space + '(' + space + digit[i] + space
        elif i == right:
            formula += op[i - 1] + space + digit[i] + space + ')' + space
        else:
            formula += op[i - 1] + space + digit[i] + space
    formula = formula[:-1]
    return formula


# 两个括号
def twoBracketFormula(count, maxnum):
    digit = Digit(count, maxnum)
    op = Operator(count)
    flag = random.randint(0, 1)
    formula = ""
    if flag == 0:
        formula = '(' + space + digit[0] + space
        for i in range(1, count):
            if i == 1 or i == 3:
                formula += op[i - 1] + space + digit[i] + space + ')' + space
            elif i == 2:
                formula += op[i - 1] + space + '(' + space + digit[i] + space
        formula = formula[:-1]
    elif flag == 1:
        area = random.randint(0, 1)  # 0表示左括号一起，1表示右括号一起
        if area == 0:
            formula += conBracket(count, formula, digit, op, '(', ')')
            formula = formula[:-1]
        elif area == 1:
            s = conBracket(count, formula, digit, op, ')', '(')
            s_list = s.split(" ")
            s_list = s_list[-1::-1]
            out = ' '.join(s_list)
            if out[0] == ' ':
                out = out[1:]
            formula += out
    return formula


def conBracket(count, formula, digit, op, str1, str2):
    left = random.randint(0, 1)
    if left == 0:
        formula += str1 + space + str1 + space + digit[0] + space
        for i in range(1, count):
            if i != count - 1:
                formula += op[i - 1] + space + digit[i] + space + str2 + space
            else:
                formula += op[i - 1] + space + digit[i] + space
    else:
        formula += digit[0] + space
        for i in range(1, count):
            if i == 1:
                formula += op[i - 1] + space + str1 + space + str1 + space + digit[i] + space
            else:
                formula += op[i - 1] + space + digit[i] + space + str2 + space
    return formula


class Change:
    exp = ""

    def suffix(self):
        if not self.exp:  # 如果传入字符串空
            print("ERROR!")
            return []
        symbol = {'+': 1,  # 用字典将四个运算符的优先级进行划分
                  '-': 1,
                  '×': 2,
                  '÷': 2
                  }
        suffix_list = []  # 后缀表达式栈
        symbol_list = []  # 字符栈
        infix = self.exp.split(' ')  # 将中缀表达式根据空格进行分割
        for i in infix:
            if i in ['+', '-', '×', '÷']:
                while len(symbol_list) >= 0:
                    if len(symbol_list) == 0:  # 如果字符栈空
                        symbol_list.append(i)
                        break
                    top = symbol_list.pop()
                    if top == '(' or symbol[top] < symbol[i]:  # 栈顶操作符优先级低于该操作符
                        symbol_list.append(top)
                        symbol_list.append(i)
                        break
                    else:
                        suffix_list.append(top)
            elif i == '(':
                symbol_list.append(i)
            elif i == ')':
                while len(symbol_list) > 0:
                    top = symbol_list.pop()
                    if top != '(':
                        suffix_list.append(top)
                    else:
                        break
            else:
                suffix_list.append(i)

        while len(symbol_list) > 0:
            top = symbol_list.pop()
            suffix_list.append(top)

        return suffix_list

    def calculate(self):
        global num
        cal_list = self.suffix()
        num_list = []
        for i in cal_list:
            if i in ['+', '-', '×', '÷']:
                first = num_list.pop()
                second = num_list.pop()
                if i == '+':
                    result = second + first
                elif i == '-':
                    result = second - first
                    if result < 0:
                        return
                elif i == '×':
                    result = second * first
                else:
                    if first == 0:
                        return
                    else:
                        result = second / first
                num_list.append(result)
            else:  # 将字符型转化为整型 将带分数转化为假分数并通过Fraction使分数之间可直接计算
                if i.find('/') > 0:
                    if i.find("'") > 0:  # 带分数
                        parts = i.split("'")  # 以带分数的点进行切割
                        attach = int(parts[0])
                        right = parts[1]
                    else:  # 若不是带分数
                        attach = 0
                        right = i
                    parts = right.split('/')
                    result = Fraction(attach * int(parts[1]) + int(parts[0]), int(parts[1]))
                    num_list.append(result)
                else:  # 若不是分数，转为整型即可
                    num_list.append(Fraction(int(i), 1))

        answer = num_list.pop()
        num += 1  # 控制题目生成个数
        print(f"题目:\n{self.exp}")
        answer_input = input("请输入答案：")
        with open('Answer_input.txt', 'a', encoding="UTF-8") as f:
            print(f"Answer_input {num}:  {answer_input}", file=f)

        with open('Exercises.txt', 'a', encoding="UTF-8") as f:
            print(f"Question {num}:  {self.exp} =", file=f)

        with open('Answers.txt', 'a', encoding="UTF-8") as f:
            print(f"Answer {num}:  {answer}", file=f)


def check(input_file, answer_file):  # 检查答案
    i = 0  # 记录题目序号
    wrong = 0  # 正确个数
    correct = 0  # 错误个数
    answer_input = []  # 输入的答案
    wrong_num = []
    correct_num = []
    with open(input_file, 'r', encoding="UTF-8") as f:
        for item in f:
            answer = re.findall(r'\d+:(.*)\n', item)  # 正则表达式进行匹配，提取出所需部分
            if answer:
                answer = answer[-1]
            else:
                continue
            answer_input.append(answer)
    with open(answer_file, 'r', encoding="UTF-8") as f:
        for item in f:
            ans = re.findall(r'\d+:(.*)\n', item)
            if ans:
                ans = ans[-1]
            else:
                continue
            if ans == answer_input[i]:  # 若输入答案和正确答案相等
                correct += 1
                correct_num.append(i + 1)
            else:
                wrong += 1
                wrong_num.append(i + 1)
            i += 1
    with open('Grade.txt', 'w', encoding="UTF-8") as f:
        correct_str = 'Correct: ' + str(correct) + str(correct_num) + '\n'
        wrong_str = 'Wrong: ' + str(wrong) + str(wrong_num) + '\n'
        f.write(correct_str)
        f.write(wrong_str)


def main():
    global num  # 控制while循环是否继续运行

    file = open('Exercises.txt', 'w').close()  # 清空上一次的内容
    file = open('Answers.txt', 'w').close()
    file = open('Answer_input.txt', 'w').close()
    file = open('Grade.txt', 'w').close()

    maxnum = int(input("请输入最大范围："))
    maxdigit = int(input("请输入生成题目个数："))  # while循环终止条件
    while num < maxdigit:
        count = random.randint(2, 4)
        if count == 2:
            question = noBracketFormula(count, maxnum)
        elif count == 3:
            choice = random.randint(0, 1)
            if choice == 0:
                question = noBracketFormula(count, maxnum)
            elif choice == 1:
                question = oneBracketFormula(count, maxnum)
        elif count == 4:
            choice = random.randint(0, 2)
            if choice == 0:
                question = noBracketFormula(count, maxnum)
            elif choice == 1:
                question = oneBracketFormula(count, maxnum)
            elif choice == 2:
                question = twoBracketFormula(count, maxnum)
        number = Change()
        number.exp = question
        number.calculate()


main()
check('Answer_input.txt', 'Answers.txt')
