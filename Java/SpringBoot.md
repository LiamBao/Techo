link:  start.spring.io

### Spring Boot 易学:
组件自动配置: 规约大于配置,专注核心业务
外部化配置: 一次构建, 按需调配, 到处运行
嵌入式容器: 内置容器, 无需部署, 独立运行
SpringBootStarter: 简化依赖,按需装配,自我包含
production-ready: 一站式运维,生态无缝整合

### Spring Boot 难精
组件自动装配: 模式注解, @Enable 模块, 条件装配, 加载机制
外部化配置: Environment抽象,生命周期, 破坏性变更
嵌入式容器: servlet web 容器, reactive web容器
Spring Boot Starter: 依赖管理, 装配条件, 装配顺序

####Spring Boot三大特性:
组件自动装配: WEB MVC Web Flux, JDBC
嵌入式Web容器: Tomcat, JEtty, undertow

核心特性:
  组件自动装配:
    激活: @EnableAutoConfiguration
    配置: /META-INF/spring.factories
    实现: xxxAutoConfiguration

#### Spring BNoot Flux运用
reactor基础: java lambda, mono, flux
web flux核心: web mvc注解, 函数式声明, 异步非租塞
