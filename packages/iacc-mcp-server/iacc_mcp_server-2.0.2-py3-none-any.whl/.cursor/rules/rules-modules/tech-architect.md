 # 🏛️ L2: 技术架构设计模块

## 📋 模块概述

**技术架构设计模块** 是IACC 2.0工作流的第二层，负责将L1层的产品需求转换为具体的技术架构设计和实现方案，确保技术选型的合理性和架构的可扩展性。

### 🎯 核心职责
- **架构设计**: 设计清晰的分层架构和系统架构
- **技术选型**: 基于需求特点选择最优技术栈
- **接口定义**: 设计详细的API接口和数据模型
- **性能规划**: 制定性能指标和扩展策略

---

## 🔄 处理流程

### 📊 输入格式
```yaml
输入类型: L1层产品需求分析结果
结构:
  parsed_requirements: "项目类型和业务领域"
  user_scenarios: "用户场景和旅程地图"
  feature_modules: "功能模块清单"
  tech_direction: "初步技术方向建议"
  complexity_score: "复杂度评估分数"
```

### ⚡ 处理逻辑
```python
class TechArchitect:
    def __init__(self):
        self.expert_selector = ExpertSelector()
        self.architecture_patterns = {
            'layered': LayeredArchitecture(),
            'microservice': MicroserviceArchitecture(),
            'hexagonal': HexagonalArchitecture(),
            'event_driven': EventDrivenArchitecture()
        }
    
    def design_architecture(self, l1_output):
        """L2层技术架构设计处理"""
        # 步骤1: 专家角色选择
        selected_experts = self.expert_selector.select_experts(l1_output)
        
        # 步骤2: 系统架构设计
        system_architecture = self.design_system_architecture(l1_output, selected_experts)
        
        # 步骤3: 技术栈确定
        tech_stack = self.finalize_tech_stack(l1_output, system_architecture)
        
        # 步骤4: 数据架构设计
        data_architecture = self.design_data_architecture(l1_output, tech_stack)
        
        # 步骤5: 接口规范定义
        api_specification = self.define_api_specification(l1_output, system_architecture)
        
        # 步骤6: 部署架构规划
        deployment_architecture = self.plan_deployment_architecture(tech_stack, l1_output.complexity_score)
        
        return {
            'selected_experts': selected_experts,
            'system_architecture': system_architecture,
            'tech_stack': tech_stack,
            'data_architecture': data_architecture,
            'api_specification': api_specification,
            'deployment_architecture': deployment_architecture
        }
```

---

## 🧠 专家角色智能选择

### 🎯 专家选择策略
```python
class ExpertSelector:
    def __init__(self):
        self.expert_mapping = {
            # 后端开发专家
            'java_backend': '/rules/back/java-expert.md',
            'go_backend': '/rules/web3/go-blockchain-expert.md',
            
            # 前端开发专家  
            'react_frontend': '/rules/front/react-expert.md',
            'vue_frontend': '/rules/front/vue-expert.md',
            
            # 移动端专家
            'android_mobile': '/rules/android/android-expert.md',
            
            # Web3专家
            'solidity_web3': '/rules/web3/solidity-expert.md',
            'solana_web3': '/rules/web3/solana-expert.md',
            
            # 产品专家
            'product_manager': '/rules/product/product-expert.md'
        }
    
    def select_experts(self, l1_output):
        """基于L1输出智能选择专家组合"""
        project_type = l1_output['parsed_requirements']['project_type']
        business_domain = l1_output['parsed_requirements']['business_domain']
        complexity_score = l1_output['complexity_score']
        
        selected_experts = []
        
        # 根据项目类型选择主要专家
        if project_type == "后端系统":
            if "高并发" in l1_output['tech_direction'] or complexity_score >= 6:
                selected_experts.append(self.expert_mapping['java_backend'])
            else:
                selected_experts.append(self.expert_mapping['java_backend'])
                
        elif project_type == "前端应用":
            if "React" in l1_output['tech_direction']:
                selected_experts.append(self.expert_mapping['react_frontend'])
            else:
                selected_experts.append(self.expert_mapping['vue_frontend'])
                
        elif project_type == "移动APP":
            selected_experts.append(self.expert_mapping['android_mobile'])
            
        elif project_type == "区块链项目":
            if "Solana" in l1_output['tech_direction']:
                selected_experts.append(self.expert_mapping['solana_web3'])
            else:
                selected_experts.append(self.expert_mapping['solidity_web3'])
                
        elif project_type == "全栈项目":
            # 全栈项目需要多个专家协作
            selected_experts.extend([
                self.expert_mapping['java_backend'],
                self.expert_mapping['react_frontend']
            ])
        
        return selected_experts
```

### 🎭 专家调用模板
```yaml
Java后台架构师调用:
  专家路径: /rules/back/java-expert.md
  调用时机: 后端系统/微服务架构设计
  提示词模板: |
    作为Java后台开发专家，请基于以下需求设计系统架构：
    
    需求背景: {l1_requirements}
    功能模块: {feature_modules}
    复杂度评估: {complexity_score}/10
    
    请提供：
    1. 分层架构设计 (Controller-Service-Repository-Entity)
    2. 微服务划分策略 (如果适用)
    3. 数据库设计和缓存策略
    4. 安全架构和权限设计
    5. 性能优化策略
    
    输出格式: 详细的技术架构文档

React前端架构师调用:
  专家路径: /rules/front/react-expert.md  
  调用时机: 前端应用架构设计
  提示词模板: |
    作为React开发专家，请基于以下需求设计前端架构：
    
    需求背景: {l1_requirements}
    功能模块: {feature_modules}
    用户交互: {user_scenarios}
    
    请提供：
    1. 组件架构设计 (原子/分子/组织/模板/页面)
    2. 状态管理策略 (Redux/Zustand/Context)
    3. 路由设计和代码分割
    4. UI组件库选择和设计系统
    5. 性能优化策略 (懒加载/缓存/CDN)
    
    输出格式: 前端架构设计文档
```

---

## 🏛️ 架构设计模式

### 📊 分层架构设计
```yaml
标准分层架构模式:
  表现层 (Presentation Layer):
    职责: 用户界面和API接口
    技术: Spring MVC / React / Vue
    组件: Controller / Component / Page
    
  业务层 (Business Layer):  
    职责: 业务逻辑和规则处理
    技术: Service / UseCase / Business Logic
    组件: Service / Manager / Handler
    
  数据访问层 (Data Access Layer):
    职责: 数据持久化和访问
    技术: Repository / DAO / ORM
    组件: Repository / Mapper / Entity
    
  基础设施层 (Infrastructure Layer):
    职责: 技术支撑和外部集成  
    技术: Database / Cache / Message Queue
    组件: Config / Util / Integration

架构约束和规则:
  依赖方向: 上层依赖下层，禁止反向依赖
  接口隔离: 层间通过接口通信，不直接依赖实现
  单一职责: 每层只处理特定类型的逻辑
  开放封闭: 对扩展开放，对修改封闭
```

### 🔄 微服务架构设计
```yaml
微服务划分策略:
  按业务域划分:
    用户服务: 用户管理/认证/权限
    订单服务: 订单处理/支付/物流
    商品服务: 商品管理/库存/分类
    
  按数据模型划分:
    每个服务独立数据库
    避免数据库层面的跨服务调用
    实现数据一致性通过事件驱动
    
  服务间通信:
    同步通信: REST API / GraphQL
    异步通信: Message Queue / Event Stream
    服务发现: Eureka / Consul / Nacos
    负载均衡: Ribbon / Gateway / Nginx

微服务技术栈:
  服务框架: Spring Boot / Spring Cloud
  API网关: Spring Cloud Gateway / Zuul
  服务注册: Eureka / Nacos / Consul  
  配置中心: Spring Cloud Config / Nacos
  熔断降级: Hystrix / Sentinel
  分布式追踪: Sleuth / Zipkin / SkyWalking
```

---

## 📊 数据架构设计

### 🗄️ 数据库设计策略
```yaml
关系数据库设计:
  主数据库选择:
    MySQL: 通用业务场景，事务性要求高
    PostgreSQL: 复杂查询，数据一致性要求极高
    SQL Server: 企业级应用，与微软技术栈集成
    
  数据库架构模式:
    单库模式: 简单应用，数据量小
    主从复制: 读写分离，提升查询性能
    分库分表: 海量数据，水平扩展
    
  表设计规范:
    主键策略: 雪花算法ID / UUID / 自增ID
    索引设计: 覆盖索引 / 联合索引 / 分区索引
    字段规范: 统一命名 / 数据类型 / 默认值

缓存架构设计:
  缓存层级:
    L1缓存: 应用内存缓存 (Caffeine / Guava)
    L2缓存: 分布式缓存 (Redis / Hazelcast)
    L3缓存: CDN缓存 (CloudFlare / 阿里云CDN)
    
  缓存策略:
    Cache-Aside: 应用控制缓存更新
    Write-Through: 写入时同步更新缓存
    Write-Behind: 异步写入，提升性能
    
  缓存一致性:
    过期策略: TTL / LRU / LFU
    更新策略: 删除缓存 / 更新缓存 / 双删除
    分布式锁: Redis分布式锁 / Zookeeper锁
```

### 📈 数据建模示例
```sql
-- 用户管理模块数据模型
CREATE TABLE users (
    id BIGINT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    status TINYINT DEFAULT 1 COMMENT '状态:1-正常,0-禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB COMMENT='用户表';

-- 角色权限模块数据模型  
CREATE TABLE roles (
    id BIGINT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='角色表';

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB COMMENT='用户角色关联表';
```

---

## 🔌 API接口设计

### 📋 接口规范定义
```yaml
RESTful API设计规范:
  URL设计:
    资源导向: /api/v1/users/{id}
    动词使用: GET/POST/PUT/DELETE
    版本控制: /api/v1/ /api/v2/
    
  请求响应格式:
    请求头: Content-Type: application/json
    认证头: Authorization: Bearer {token}
    响应格式: 统一JSON格式包装
    
  状态码规范:
    200: 请求成功
    201: 创建成功  
    400: 请求参数错误
    401: 认证失败
    403: 权限不足
    404: 资源不存在
    500: 服务器内部错误

API接口示例:
  用户管理接口:
    POST /api/v1/users - 创建用户
    GET /api/v1/users/{id} - 获取用户详情
    PUT /api/v1/users/{id} - 更新用户信息
    DELETE /api/v1/users/{id} - 删除用户
    GET /api/v1/users?page=1&size=20 - 分页查询用户
    
  认证授权接口:
    POST /api/v1/auth/login - 用户登录
    POST /api/v1/auth/refresh - 刷新令牌
    POST /api/v1/auth/logout - 用户退出
```

### 📄 OpenAPI文档示例
```yaml
openapi: 3.0.0
info:
  title: 企业级CRM系统API
  version: 1.0.0
  description: 客户关系管理系统的RESTful API

paths:
  /api/v1/users:
    post:
      summary: 创建用户
      tags: [用户管理]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [username, email, password]
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 50
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        201:
          description: 用户创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'

components:
  schemas:
    UserResponse:
      type: object
      properties:
        code:
          type: integer
          example: 200
        message:
          type: string
          example: "success"
        data:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
```

---

## 🚀 部署架构规划

### 🐳 容器化部署策略
```yaml
Docker容器化:
  应用镜像:
    基础镜像: openjdk:11-jre-slim / node:16-alpine
    多阶段构建: 分离构建和运行环境
    镜像优化: 层缓存 / 减少镜像大小
    
  容器编排:
    本地开发: docker-compose
    生产环境: Kubernetes / Docker Swarm
    服务网格: Istio / Linkerd (复杂度>=8)

Kubernetes部署:
  资源配置:
    Deployment: 应用部署和滚动更新
    Service: 服务发现和负载均衡  
    Ingress: 外部访问和路由规则
    ConfigMap/Secret: 配置管理和密钥管理
    
  监控告警:
    指标收集: Prometheus + Grafana
    日志聚合: ELK Stack / Loki
    链路追踪: Jaeger / SkyWalking
    告警通知: AlertManager + 钉钉/企微
```

---

## 📊 L2层输出标准

### 🎯 技术架构设计文档
```yaml
L2_技术架构设计结果:
  专家团队配置:
    主导专家: "Java后台开发专家" | "React前端专家" | "Android专家" | "Web3专家"
    协作专家: ["数据库专家", "DevOps专家"] (可选)
    专家调用路径: ["/rules/back/java-expert.md"]
    
  系统架构设计:
    架构模式: "分层架构" | "微服务架构" | "六边形架构" | "事件驱动架构"
    架构图: "详细的系统架构图 (draw.io格式)"
    模块划分: 
      - 核心模块: ["用户模块", "业务模块", "数据模块"]
      - 支撑模块: ["权限模块", "配置模块", "监控模块"]
    接口设计: "模块间接口定义和通信协议"
    
  技术栈确定:
    前端技术栈:
      框架: "React 18 + TypeScript" | "Vue 3 + TypeScript"
      状态管理: "Redux Toolkit" | "Pinia" | "Zustand"
      UI组件库: "Ant Design" | "Element Plus" | "Material-UI"
      构建工具: "Vite" | "Webpack" | "Turbopack"
    后端技术栈:
      框架: "Spring Boot 2.7 + Java 11" | "Go 1.19 + Gin"
      ORM框架: "MyBatis Plus" | "Spring Data JPA" | "GORM"
      安全框架: "Spring Security + JWT" | "Shiro"
      服务框架: "Spring Cloud" | "Dubbo" (微服务场景)
    数据存储:
      主数据库: "MySQL 8.0" | "PostgreSQL 14" | "MongoDB 5.0"
      缓存数据库: "Redis 6.2" | "Hazelcast"
      搜索引擎: "Elasticsearch 8.0" (如需要)
      消息队列: "RocketMQ" | "Kafka" | "RabbitMQ" (如需要)
      
  数据架构设计:
    数据库设计:
      ER图: "完整的实体关系图"
      表结构: "详细的表结构设计 (DDL脚本)"
      索引策略: "主键/唯一索引/复合索引设计"
      分库分表: "水平分片/垂直分片策略" (如需要)
    缓存架构:
      缓存层级: "L1应用缓存 + L2分布式缓存"
      缓存策略: "Cache-Aside" | "Write-Through" | "Write-Behind"
      缓存一致性: "TTL过期 + 主动更新"
      
  API接口规范:
    接口设计:
      协议规范: "RESTful API" | "GraphQL API" | "gRPC API"
      认证授权: "JWT Token" | "OAuth2.0" | "API Key"
      版本管理: "URL版本" | "Header版本"
      限流策略: "令牌桶" | "滑动窗口" | "漏桶算法"
    接口文档:
      文档格式: "OpenAPI 3.0规范"
      接口清单: ["用户接口", "业务接口", "系统接口"]
      请求响应: "统一JSON格式包装"
      错误处理: "统一错误码和错误信息"
      
  部署架构规划:
    容器化:
      镜像策略: "多阶段构建 + Alpine基础镜像"
      编排工具: "Docker Compose" | "Kubernetes" | "Docker Swarm"
      服务发现: "Consul" | "Eureka" | "K8s Service"
    CI/CD:
      构建工具: "Jenkins" | "GitLab CI" | "GitHub Actions"
      部署策略: "蓝绿部署" | "滚动更新" | "金丝雀发布"
      环境管理: "开发/测试/预生产/生产环境"
    监控运维:
      应用监控: "Prometheus + Grafana"
      日志管理: "ELK Stack" | "Loki + Grafana"
      链路追踪: "SkyWalking" | "Jaeger" | "Zipkin"
      告警通知: "邮件/短信/钉钉/企微通知"
```

---

## ✅ L2层质量检查

### 🔍 架构设计质量标准
```yaml
架构设计合规性检查:
  ✅ 分层架构清晰 (严格按照DDD/分层架构设计)
  ✅ 模块职责单一 (每个模块职责明确，高内聚低耦合)
  ✅ 接口设计合理 (符合RESTful规范，接口幂等性)
  ✅ 依赖关系清晰 (上层依赖下层，避免循环依赖)

技术选型合理性检查:
  ✅ 技术栈匹配度高 (与业务需求和复杂度匹配)
  ✅ 框架版本稳定 (选择LTS版本，避免过新或过旧)
  ✅ 生态兼容性好 (框架间兼容，社区活跃)
  ✅ 团队技能匹配 (考虑团队现有技能和学习成本)

数据架构合规性检查:
  ✅ 数据模型规范 (符合三范式，避免数据冗余)
  ✅ 索引设计合理 (覆盖查询场景，避免过度索引)
  ✅ 缓存策略得当 (缓存命中率>80%，缓存一致性保证)
  ✅ 数据安全保障 (敏感数据加密，备份恢复策略)

接口设计质量检查:
  ✅ API规范标准 (符合OpenAPI 3.0规范)
  ✅ 认证授权完整 (JWT/OAuth2实现，权限控制细粒度)
  ✅ 错误处理统一 (错误码规范，错误信息友好)
  ✅ 接口性能优化 (分页查询，批量操作，响应时间<200ms)
```

---

**🏛️ L2技术架构设计模块通过智能专家选择和严格的架构设计规范，确保技术方案的合理性、可扩展性和可维护性，为L3层的代码实现提供清晰的技术蓝图。**