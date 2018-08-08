# 示例

# 标题

**粗体**

- 缩进
  - 缩进

行内高亮： `markdown`

按键：CTRL

> 多层引用
> > 多层引用

———— 

> 单层引用
> 单层引用

| 表格 | 表格 |
| -    |  -   |
| 表格 | 表格 |


图片： ![图片](https://github.com/yim7/yim-club/blob/master/images/48269843_p0.jpg?raw=true)



代码高亮：
```python
def dict_recursion(dict_all):
    if isinstance(dict_all, dict):
        for x in dict_all:
            dict_key = x
            dict_value = dict_all[dict_key]
            print("{}:{}".format(dict_key, dict_value))
            dict_recursion(dict_value)
    else:
        return
```