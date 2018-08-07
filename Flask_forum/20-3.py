'''
性能
1. web性能 选择的并不是性能最高的语言 节省服务器
2. web性能组成
    吴多益 打开浏览器，点击百度，搜了一个query，返回了结果
    那么发生了什么事情？

    1. 发了一个request
    2. 到达了负载均衡
    3. 到达了nginx   运维关心
    4. 到达了web server gunicorn web框架开发者 request解析，路由转发
    5. 发送了你的web server app ： application层面要跑得快
    6. web server app做了各种事情，返回了response 前端工程师

    服务器处理的时间
    7. 动态产生一堆页面，客户端渲染

3. 性能本身以后评测标准
    1. 说明硬件，某种网络设备
    2. 性能测试的时候切忌方法
        1. benchmark程序，已经跑满，而你的app没有跑满
        2. 多个客户端，每个客户端可能有几个链接
    3. 指标 每秒处理多少个请求

    框架作者喜欢测试hello world ？因为hello world本身解析请求，路由

4. ab这个工具 apache benchmark
'''

'''
测试case
1. 需要模拟有性能瓶颈的情况，topic all做一下sleep
2. 做优化的方法 cache
    a. 有一个操作很耗时，那么我们应该结果cache，下一次就很快了
    b. cache肯定不是永久有效的，topic来说，你每次改的时候都会失效
    c. 在每次失效的时候更新cache

1. 我们用内存直接cache
2. 我们不用内存，用reids
    以前我们做cache的时候，memcached
    现在redis

1. 发现问题所在，profiling
2. 根据这个问题去做bench
3. 做cache
4. 注意安全
'''