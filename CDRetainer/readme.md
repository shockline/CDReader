# CDRetainer
(A ProxyPool Retainer on Python)   
- You set several urls.
- then **CDRetainer** will crawl free proxylist from network *automatically*.
- After filter function, make a proxylist for each target.

-------------------

### Usage    

```python
git clone https://github.com/okcd00/CDRetainer.git
cd CDRetainer
vim sourcelist.txt # Change conf by yourself, default 3 targets
vim conf/Basic.conf # Change paras by yourself, default run once per 43200 seconds
nohup python CDRetainer.py &
# Then get Result in "./data"
```

### Dependency
+ [Python](http://www.python.org/)
+ `urllib2` Replaced with `urllib.request` in `python3.x`
+ `ConfigParser`  Replaced with `configparser` in `python3.x`

### New Idea
- [x] Solve Initial issue
- [x] Make a `Configure` out of Source Code
- [x] Custom `Sourcelist` for different aims

### UpdateLog    
[2015/12/18] ver 1.0.4
- Remove `PCP` Function for Poor performance
+ Add `Sup`(`Support` or `SubProcess`) Module for Issue `Errno.110`

[2015/12/07] ver 1.0.3
+ Add `Try-Except` to protect and monitor
+ Add `PCP` Function as Formula
+ Add Check-and-Retry for Empty Return

[2015/11/25] ver 1.0.2
- Remove Access Rate
+ Add switch for `PCP`(use Proxy to Capture Proxy)

[2015/11/11] ver 1.0.1
+ Fix Division Operation for ZeroDivisionError

[2015/11/10] ver 1.0.0
+ Add `Basic.conf` Config Function
+ Demo with `Logger` Complete
