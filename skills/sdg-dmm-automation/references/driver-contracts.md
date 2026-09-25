# 驱动接口契约

## VISA基类

建议使用统一基类保存：

- `resource`：`auto`或显式VISA资源地址。
- `timeout_ms`：通信超时。
- `expected_idn_contains`：型号匹配字符串。
- `resource_manager_factory`：Fake VISA注入点。
- `resource_name`、`idn`、`serial_number`、`instrument`和配置快照。

连接规则：

1. `auto`时调用`list_resources()`。
2. 逐个打开候选资源并查询`*IDN?`。
3. SDG只接受IDN型号字段精确为SDG6052X或SDG6032X-E；可选型号约束也必须匹配。不按字符串包含猜测SDG型号。
4. 0台匹配时列出已发现资源；多台匹配时要求显式资源地址。
5. 显式资源也必须查询并校验`*IDN?`，不能只相信地址。

## 信号源接口

实现以下方法：

```python
connect()
identify()
configure_dc(enable_output=True)
apply_voltage(voltage_v)
output_off()
set_safe_output()
query_error()
close()
```

`configure_dc`必须返回配置快照；`apply_voltage`必须回读目标值；`set_safe_output`必须尝试设置0 V并关闭输出，即使第一步失败也要继续尝试第二步并汇总异常。

## 万用表接口

实现以下方法：

```python
connect()
identify()
configure(...)
measure_voltage(code=None, sequence_id=None)
autozero_once()
query_error()
raise_for_error_queue()
close()
```

`measure_voltage`的最小事务是：

```python
self._write("INIT")
self._write("*TRG")
raw = self._query("FETC?")
```

解析后拒绝非有限值、不可转换值、过量程标志和超过允许电压范围的读数。

## 能力字段

每个驱动至少声明：

```python
model_key
display_name
qualification_eligible
uses_periodic_autozero
```

`qualification_eligible`只能由项目策略和测量证据决定，不能因为驱动实现了`measure_voltage`就自动设为真。

## Fake VISA要求

Fake VISA至少记录：

- 所有写入命令及顺序；
- 查询命令及返回值；
- 资源发现列表；
- 每个资源的IDN；
- 可注入超时、回读不一致、错误队列和异常读数。

测试应断言完整命令序列，而不只断言最终读数。
