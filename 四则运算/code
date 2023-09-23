x = 0  # 全局变量


class Change:
    exp = "3 + 2 - 2 + 3 * 2"

    def suffix(self):
        if not self.exp:  # 如果传入字符串空
            print("ERROR!")
            return []
        symbol = {'+': 1,  # 用字典将四个运算符的优先级进行划分
                  '-': 1,
                  '*': 2,
                  '/': 2
                  }
        suffix_list = []  # 后缀表达式栈
        symbol_list = []  # 字符栈
        infix = self.exp.split(' ')  # 将中缀表达式根据空格进行分割

        for i in infix:
            if i in ['+', '-', '*', '/']:
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
        global x
        cal_list = self.suffix()
        num_list = []
        for i in cal_list:
            if i in ['+', '-', '*', '/']:
                first = int(num_list.pop())  # 将字符变成整数取出
                second = int(num_list.pop())
                if i == '+':
                    result = second + first
                elif i == '-':
                    result = second - first
                elif i == '*':
                    result = second * first
                else:
                    if first == 0:
                        return
                    else:
                        result = second / first
                num_list.append(result)
            else:
                num_list.append(i)

        answer = num_list.pop()

        if answer < 0:
            return
        else:
            x += 1
            with open('D:\\pythonProject\\四则运算\\Exercises.txt', 'a', encoding="UTF-8") as f:
                print(f"Question {x}:  {self.exp} =", file=f)
            with open('D:\\pythonProject\\四则运算\\Answers.txt', 'a', encoding="UTF-8") as f:
                print(f"Answer {x}:  {answer}", file=f)

        print(f"{answer}")
    # return int(num_list.pop())


number = Change()
number.calculate()
