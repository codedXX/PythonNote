# Python 核心语法：流程控制

> **学习目标：** 根据条件选择分支，使用循环处理重复任务，并正确控制循环退出。

## 条件判断

`if` 根据条件是否为真执行代码块，缩进决定代码块范围。`elif` 按顺序判断，因此更严格的条件必须放在前面。

```python
if score >= 85:
    level = "优秀"
elif score >= 60:
    level = "及格"
else:
    level = "不及格"
```

## 模式匹配

`match...case`（Python 3.10+）适合对固定值或结构分类；`case _` 用作兜底分支。

* `match...case` 类似其他语言中的 `switch`。

**match...case基本写法：**

```py
score = 85

match score:
    case 100:
        level = "满分"
    case 85:
        level = "优秀"
    case 60:
        level = "及格"
    case _:
        level = "其他"

print(level)
```

`case _` 中的 `_` 表示“其他所有情况”，类似 `default`。

## 循环

### while循环

**Python 中 `while` 循环的基本写法是：**

```py
while 条件:
    要重复执行的代码
```

**例如：**

```py
number = 1

while number <= 5:
    print(number)
    number += 1
```

**输出：**

```py
1
2
3
4
5
```

执行过程是：只要 `number <= 5`，就不断执行循环体；每次加 `1`，直到条件不成立。



⭐️**注意：**

- `while` 后面要加冒号 `:`
- 循环体必须缩进
- 要改变条件相关的变量，否则可能形成无限循环



⭐️**也可以使用 `break` 提前结束：**

```py
while True:
    text = input("请输入 quit 退出：")

    if text == "quit":
        break

    print("你输入了：", text)
```

### for循环

`while` 适合“条件满足就继续”的任务，必须设计更新或退出条件；`for` 适合遍历字符串、列表等可迭代对象。`range(end)` 生成 `0` 到 `end - 1`，`range(start, end, step)` 不包含 `end`。

```python
total = 0
for number in range(1, 101):
    if number % 2:
        total += number
```

> **含义：**
>
> - `range(1, 101)`：生成 `1` 到 `100`，不包含 `101`

> ⭐️`什么情况需要加冒号？`
>
> * 不是所有语句都要加冒号，只有表示“代码块开始”的语句需要加冒号
>
>   ~~~py
>   if 条件:
>   for 变量 in 序列:
>   while 条件:
>   def 函数名():
>   class 类名:
>   try:
>   else:
>   elif 条件:
>   ~~~
>
>   



> **range(...) 语句的作用是什么？**
>
> - 生成指定规则的数字序列
>
> - 用法：
>   - range(end)
>   - range(start, end)
>   - range(start, end, step)

## 嵌套与控制语句

⭐️嵌套循环中外层通常控制行或批次，内层控制列或单项。`break` 结束`当前循环`，`continue` 跳过`本次循环其余代码`。

> ⭐️⭐️**重点：** `break` 只跳出`最内层循环`。编写登录、猜数字等逻辑时，先明确成功、失败和退出条件，避免死循环。



例如：

~~~py
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)
~~~



> ⭐️⭐️⭐️⭐️⭐️**break和continue的区别！！**
>
> *  可以这样理解：
>
>   - `break`：**彻底结束当前所在的循环**
>   - `continue`：**跳过本次循环，直接进入下一次循环**
>
>   注意：在嵌套循环中，它们只影响**当前这一层循环**。
>
>   ```py
>   for i in range(3):          # 外层循环
>       for j in range(5):      # 内层循环
>           if j == 2:
>               break           # 结束内层循环
>           print(i, j)
>           
>   ===============打印结果=================================
>   
>   0 0
>   0 1
>   1 0
>   1 1
>   2 0
>   2 1
>   ```
>
>   当 `j == 2` 时，内层循环结束，但外层循环仍会继续执行。
>
>   ```py
>   for i in range(3):
>       for j in range(5):
>           if j == 2:
>               continue        # 跳过本次内层循环
>           print(i, j)
>   
>   ===============打印结果=================================
>   
>   0 0
>   0 1
>   0 3
>   0 4
>   1 0
>   1 1
>   1 3
>   1 4
>   2 0
>   2 1
>   2 3
>   2 4
>   ```
>
>   当 `j == 2` 时，只是不执行本次循环后面的代码，接着处理 `j == 3`。
>
>   简单记忆：
>
>   ```py
>   break     = 不做了，结束当前循环
>   continue  = 这次跳过，继续下一次循环
>   ```



> ⭐️`break 关键字的作用？`
>
> - 不能够单独书写，只能出现在循环中，表示结束、跳出的意思。
>
> ⭐️`continue 关键字的作用？`
>
> - 不能够单独书写，只能出现在循环中，表示中断本次循环，直接进入下一次循环。
