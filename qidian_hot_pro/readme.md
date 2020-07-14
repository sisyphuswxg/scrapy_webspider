
* CSS 解析


* 使用Item封装数据（对比使用字典）
    * 使用字典：字段名拼写容易出错且无法检测到这些错误
    * 返回的数据类型无法确保一致性
    * 不便于将数据传递给其他组件（如传递给用于数据处理的pipeline组件）

* ItemLoader 填充数据（先解析，再构造数据 -> 使用ItemLoader将数据提取和数据封装在一起）
通过填充容易，可以配置Item中每个字段的提取规则，并通过函数分析原始数据，最后对Item进行赋值
代码量更小，更加清晰
实例化ItemLoader时，ItemLoader接受一个Item实例来指定要加载的Item（参数item）；指定response或selector来确定要解析的内容（参数response或selector）


* Pipeline
数据处理/清洗，如过滤掉重复数据、验证数据的有效性、以及将数据存入数据库等
可选功能，默认是关闭的，需要到配置文件中进行打开
可以定义多个Item Pipeline组件，数据会依次访问每个组件，执行相应的数据处理功能


* MySQL数据库
```bash
pip3 install mysqlclient
MySQLPipeline
```


* MongoDB数据库

使用社区版 
```bash
# install mongodb
brew tap mongodb/brew
brew services start mongodb-community

# 可视化工具
brew cask install mongodb-compass

pip3 install pymongo
MongoDBPipeline
```


* Redis数据库

```bash
pip install redis==2.10.6
RedisPipeline
```
