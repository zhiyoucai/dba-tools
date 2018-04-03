## CheckPool的使用方法

```bash
# 用来计算2秒内的均值
python CheckPool.py --host 127.0.0.1 --port 3306 --type qps  --user root --pass 123456 --db test --interval 2 --avg True

# 用来计算2秒内的delta值
python CheckPool.py --host 127.0.0.1 --port 3306 --type qps  --user root --pass 123456 --db test --interval 2
```