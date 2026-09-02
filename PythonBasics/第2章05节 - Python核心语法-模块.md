# Python 核心语法：模块与包

> **学习目标：** 按职责拆分代码，通过导入复用功能，并理解模块执行入口。

# 模块

* Python模块(module)：一个.py文件就是一个模块，模块是Python程序的基本组织单位。在模块中可以定义变量、函数、类，以及可执行的代码。

作用

* 提高代码复用性
* 降低开发门槛
* 避免命名冲突



## 导入模块

* 在使用模块中提供的功能之前，必须得先导入，再使用。
* 导入模块的具体语法如下：

| 导入形式                          | 代码样例                           | 调用方式        | 调用方式                |
| --------------------------------- | ---------------------------------- | --------------- | ----------------------- |
| import 模块名                     | import random, os                  | `模块名.功能名` | random.randint(10, 100) |
| import 模块名 as 别名             | import random as rd                | 别名.功能名     | rd.randint(10, 100)     |
| from 模块名 import 功能名         | from random import randint, choice | 功能名          | randint(10, 100)        |
| from 模块名 import 功能名 as 别名 | from random import randint as rint | 别名            | rint(10, 100)           |
| from 模块名 import *              | from random import *               | `功能名`        | randint(10, 100)        |



**小结**

* 什么是模块? 有什么用?
  * 模块：就是一个python文件(.py)，其中就包含了变量、函数、类，以及可执行的代码。
  * 作用：提高代码复用性，降低开发门槛

* 导入模块的常用语法? 
  * import 模块名 [as 别名]
  * from 模块名 import 功能名 [as 别名]
  * from 模块名 import *

## 自定义模块

当开发一些复杂的项目，为了让项目结构更清晰，更便于项目的维护管理 及 代码的复用，可能会把一个项目拆分为若干个模块。

~~~python
"""自定义模块示例：拆分前

所有功能和主程序都写在同一个文件中。
"""


def calculate_average(scores):
    """计算成绩平均分。"""
    if not scores:
        return 0

    return sum(scores) / len(scores)


def is_passed(average):
    """判断平均分是否及格。"""
    return average >= 60


scores = [80, 75, 90, 55]
average = calculate_average(scores)

print(f"平均分：{average:.2f}")
print("是否及格：", "是" if is_passed(average) else "否")

~~~

> * 这是 Python 的**条件表达式（三元表达式）**：
>
>   ~~~python
>   "是" if is_passed(average) else "否"
>   ~~~
>
> * `sum()` 是 Python 中用于**求和**的内置函数。



**可以拆分为**

`自定义模块_拆分后.py`

```python
"""自定义模块示例：拆分后

具体功能放在 score_utils.py 中，当前文件只负责调用功能。
"""

from score_utils import calculate_average, is_passed


scores = [80, 75, 90, 55]
average = calculate_average(scores)

print(f"平均分：{average:.2f}")
print("是否及格：", "是" if is_passed(average) else "否")
```

`score_utils.py`

```python
"""成绩相关的工具函数。"""


def calculate_average(scores):
    """计算成绩平均分。"""
    if not scores:
        return 0

    return sum(scores) / len(scores)


def is_passed(average):
    """判断平均分是否及格。"""
    return average >= 60
```

> **为什么可以直接写from score_utils ，不应该写from ./score_utils  吗？** 
>
> 
>
> `Python 会自动把当前执行文件所在的目录加入模块搜索路径`，所以可以直接写：
>
> ```
> from score_utils import calculate_average
> ```
>
> 意思是：
>
> ```
> 从 score_utils.py 文件中导入 calculate_average 函数
> ```
>
> `from .score_utils import ...` 中的 `.` 才表示“当前包目录”，但它通常用于包结构中：
>
> ```
> from .score_utils import calculate_average
> ```
>
> 而下面这种写法是错误的：
>
> ```
> from ./score_utils import calculate_average
> ```
>
> 简单区分：
>
> ```
> from score_utils import func      # 导入同目录或搜索路径中的模块
> from .score_utils import func     # 使用相对导入，. 表示当前包
> ```
>
> 对于目前这个简单示例，使用：
>
> ```
> from score_utils import calculate_average, is_passed
> ```
>
> 即可。
>
> 

> 
>
> 注意：每一个python文件都可以作为一个模块，`模块的名字就是文件的名字`（建议使用python标识符定义，规范命名） 。



### _ all _

**_ all _是一个模块级别的特殊变量，用于指定 from 模块名 import * 时会导入哪些功能(*通配了哪些功能)。**



 `__all__`，它用于指定模块允许被 `import *` 导入的内容。

在 `score_utils.py` 中：

```python
__all__ = ["calculate_average", "is_passed"]


def calculate_average(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


def is_passed(average):
    return average >= 60


def _debug():
    print("调试信息")
```

在其他文件中：

```python
from score_utils import *

print(calculate_average([80, 90]))
print(is_passed(75))

# _debug()  # 不会被 * 导入
```

`__all__` 的意思是：

```python
当别人使用 from score_utils import * 时，只导入列表中的内容。
```

不过更推荐明确导入：

```python
from score_utils import calculate_average, is_passed
```

注意，`__all__` 两边是**两个下划线**：

```python
__all__
```



> 注意：__all__控制的是 from ... import * 时，要导入的功能，并不会影响直接导入具体的功能（如: from ... import 功能） 。



### __ name __

`__name__`：判断文件是直接运行还是被导入

```python
print(__name__)
```

如果直接运行文件：

```python
python demo.py
```

输出通常是：

```python
__main__
```

如果被其他文件导入：

```python
import demo
```

此时 `demo.py` 中的 `__name__` 是：

```python
demo
```

因此常见写法是：

```python
def main():
    print("程序开始运行")


if __name__ == "__main__":
    main()
```

含义是：

```python
只有直接运行这个文件时，才执行 main()
如果这个文件被导入，就不自动执行 main()
```

这样可以避免导入模块时，模块中的测试代码或主程序代码自动运行。



#### 小结

1. __ name__ 与 __ all __  这两个特殊变量的作用是什么？
   - __ name __是 Python 中非常重要的内置变量，表示的是当前模块的名称。
     - 当模块直接运行时：`__name__` 的值为 `"__main__"`（`if __name__ == "__main__"`）。
     - 当模块被导入时：`__name__` 等于模块的文件名（不含 `.py` 后缀）。
   - `__all__`：控制 `import *` 时导入哪些功能。

## 软件包(package)

* 包：本质就是一个文件夹，该`文件夹中可以包含若干python模块（.py文件）`，文件夹下还包含了一个__init__.py。
* 作用：`模块文件较多时`，`用来管理多个模块`。（包的本质也是一个模块）



| 导入形式                       | 代码样例                                | 调用方式           | 调用方式                      |
| ------------------------------ | --------------------------------------- | ------------------ | ----------------------------- |
| import 包名.模块名             | import utils.my_fun                     | 包名.模块名.功能名 | utils.my_fun.log_separator1() |
| from 包名 import 模块名        | from utils import my_fun                | 模块名.功能名      | my_fun.log_separator1()       |
| from 包名 import *             | from utils import *                     | 模块名.功能名      | my_fun.log_separator1()       |
| from 包名.模块名 import 功能名 | from utils.my_fun import log_separator1 | 功能名             | log_separator1()              |
| from 包名.模块名 import *      | from utils.my_fun import *              | 功能名             | log_separator1()              |

> **注意：** 在通过 `from 包名 import *` 导入全部模块的时候，需要在 `__init__.py` 文件中添加 `__all__=[]`，控制允许导入的模块列表。





`Python 中的软件包（package），就是用来组织多个模块的文件夹。`

可以把它理解为：

```python
模块 module  = 一个 .py 文件
软件包 package = 一个包含多个模块的文件夹
```

例如：

```python
project/
├── main.py
└── tools/
    ├── __init__.py
    ├── math_utils.py
    └── string_utils.py
```

这里：

- `tools` 是软件包
- `math_utils.py` 是模块
- `string_utils.py` 是模块
- `__init__.py` 表示这是一个 Python 软件包

在 `main.py` 中可以这样导入：

```python
from tools.math_utils import add
from tools.string_utils import to_upper
```

也可以写成：

```python
import tools.math_utils

result = tools.math_utils.add(1, 2)
```

`__init__.py` 可以是空文件，也可以用于导出常用函数：

```python
# tools/__init__.py
from .math_utils import add
```

这样就可以简化导入：

```python
from tools import add
```

软件包的主要作用是：

- 把相关模块放在一起
- 让项目目录更清晰
- 避免不同模块重名
- 方便代码复用和维护

常见的第三方软件包包括：

```python
import requests
import numpy
import pandas
```

它们都是别人已经写好的 Python 软件包。





#### 小结

1. 什么是包？有什么作用？
   - 包就是一个文件夹，里面可以存储很多 Python 模块（`.py` 文件），通过包可以对模块进行归类。
2. __ init __.py 文件的作用？
   - 标识这是一个包，而不是普通的文件夹。
   - 控制在 `import *` 时导入的模块列表（`__all__` 变量）。
3. 导入包的方式？
   - `import 包名.模块名`
   - `from 包名 import 模块名`
   - `from 包名 import *`
   - `from 包名.模块名 import 功能名`
   - `from 包名.模块名 import *`
