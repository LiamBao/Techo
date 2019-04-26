# asynicio

[https://www.jianshu.com/p/b5e347b3a17c](https://www.jianshu.com/p/b5e347b3a17c)

## asynicio

_**event\_loop**_ 事件循环：程序开启一个无限的循环，程序员会把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。 _**coroutine**_ 协程：协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。 _**task**_ 任务：一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含任务的各种状态。 _**future**_ 代表将来执行或没有执行的任务的结果。它和task上没有本质的区别 _**async/await**_ 关键字：python3.5 用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口 _**并发**_ 通常指有多个任务需要同时进行 _**并行**_ 则是同一时刻有多个任务执行

asyncio.ensure\_future\(coroutine\) 和 loop.create\_task\(coroutine\)都可以创建一个task

