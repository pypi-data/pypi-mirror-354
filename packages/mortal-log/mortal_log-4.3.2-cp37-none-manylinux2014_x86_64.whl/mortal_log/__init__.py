#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 18:05
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalLog"]
from .log_main import MortalLog
"""
MortalLog: 增强日志类，创建或获取日志器实例
   参数:
      name: 日志器名称，如果为None或非字符串则使用"root"
      level: 日志级别，默认为DEBUG
      file: 日志文件路径，None表示不记录到文件
      handler_type: 文件处理器类型，可选值["file", "rotating", "timerotating"]
      console: 是否输出到控制台，默认为True
      rehandler: 是否重新处理现有日志器的处理器，默认为False
      **kwargs: 其他传递给文件处理器的参数
         mode: 
         encoding: 
         maxBytes: 
         backupCount: 
         when: 
         interval: 
   可用方法: 
      xxx.debug(*message, args=None, kwargs=None): 记录DEBUG级别日志
      xxx.info(*message, args=None, kwargs=None): 记录INFO级别日志
      xxx.warning(*message, args=None, kwargs=None): 记录WARNING级别日志
      xxx.error(*message, args=None, kwargs=None): 记录ERROR级别日志
      xxx.critical(*message, args=None, kwargs=None): 记录CRITICAL级别日志
      
      xxx.set_console_level(level): 设置控制台处理器日志级别
      xxx.set_file_level(level): 设置文件处理器日志级别
      xxx.disable(): 禁用日志器，内部方法，不要使用，以免造成实例损坏
      xxx.enable(value): 启用日志器，内部方法，不要使用，以免造成实例损坏
      xxx.close(): 关闭日志器并清理资源

例子: 
   log = MortalLog(name="file", file=os.path.join(os.getcwd(), "log.log"), console=True)
   ==> 实例化一个带文件处理器及控制台处理器的日志器
   
   log.set_file_level(30)
   ==> 设置文件处理器日志级别为 WARNING (10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL)
   
   log.set_console_level(30)
   ==> 设置控制台处理器日志级别为 WARNING ，如未设置输出到控制台，则无效但不报错
   
   log.debug(1, 2, 3, 4)
   ==> 输出: '2025-06-12 16:57:53,346 - file - INFO - 1 2 3 4'
   
   log.info("Hello", "World!")
   ==> 输出: '2025-06-12 16:57:53,346 - file - INFO - Hello World!'
   
   log.warning("Hello, World!")
   ==> 输出: '2025-06-12 16:57:53,346 - file - INFO - Hello, World!'
   
   log.error(log)
   ==> 输出: '2025-06-12 16:57:53,346 - file - INFO - ${log实例的__str__}'
   
   log.critical("test")
   ==> 输出: '2025-06-12 16:57:53,346 - file - INFO - test'
   
   log.close()
   ==> 关闭日志器并清理资源，以上方法再次调用无输出也无报错，如: 再次调用 log.critical("test") 无输出也不会报错，实例已禁用
"""
