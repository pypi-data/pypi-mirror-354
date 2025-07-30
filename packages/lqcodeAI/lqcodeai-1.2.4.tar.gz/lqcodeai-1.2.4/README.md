# lqcode_sdk包使用说明

## 安装sdk
```bash
pip install lqcodeAI
```

## 导入包
```python
from lqcodeAI import lq


```

## 基本使用

### 0. 访问密码
``` python
password = 'lqcode'  # 访问密码
```

### 1. 藏头诗生成功能
```python
result = lq.ai_poetry(password, name)
```
参数说明：
- password: 访问密码（字符串）
- name: 藏头诗内容（字符串，默认为"李梅"）

返回值说明：
```python
{
    "poem": "生成的诗词内容",
    "explanation": "诗词解释"
}
```

示例：
```python
# 生成"李梅"的藏头诗
result = lq.ai_poetry(password, "李梅")
print(result)
# 输出示例：
# {
#     "poem": "李白乘舟将欲行，\n梅子黄时雨。\n...",
#     "explanation": "这是一首描写春天景色的诗..."
# }
```

### 2. 天气查询功能
```python
result = lq.ai_weather(password, city)
```
参数说明：
- password: 访问密码（字符串）
- city: 城市名称（字符串）

返回值说明：
```python
{
    "weather_info": "天气信息",
    "explanation": "天气解释"
}
```

示例：
```python
# 查询北京的天气
result = lq.ai_weather(password, "北京")
print(result)
# 输出示例：
# {
#     "weather_info": "晴，25℃，湿度45%，东南风3级",
#     "explanation": "今天北京天气晴朗，适合外出活动..."
# }
```

### 3. B站热榜功能
```python
result = lq.ai_biliranking(password)
```
参数说明：
- password: 访问密码（字符串）

返回值说明：
```python
{
    "ranking": "B站热榜数据"
}
```

示例：
```python
# 获取B站热榜
result = lq.ai_biliranking(password)
print(result)
# 输出示例：
# {
#     "ranking": "1. 【原神】新角色演示\n2. 【英雄联盟】S12总决赛\n3. 【美食】家常菜教程..."
# }
```

### 4. 成语接龙功能
```python
result = lq.ai_idioms(password, idiom)
```
参数说明：
- password: 访问密码（字符串）
- idiom: 起始成语（字符串）

返回值说明：
```python
{
    "idiom": "接龙的成语",
    "explanation": "成语解释"
}
```

示例：
```python
# 从"一心一意"开始接龙
result = lq.ai_idioms(password, "一心一意")
print(result)
# 输出示例：
# {
#     "idiom": "意气风发",
#     "explanation": "形容精神振奋，气概豪迈..."
# }
```

## 错误处理
所有功能在遇到错误时会抛出 ValueError 异常，建议使用 try-except 进行错误处理：
```python
try:
    result = lq.ai_poetry(password, "李梅")
    print(result)
except ValueError as e:
    print(f"发生错误: {e}")
```

## 注意事项
1. 所有功能都需要提供有效的密码
2. 输入参数必须是字符串类型
3. 建议对返回结果进行错误检查
4. 可以根据需要设置重试次数（部分功能支持）

