 # ⚙️ L3: 代码实现模块

## 📋 模块概述

**代码实现模块** 是IACC 2.0工作流的第三层，负责将L2层的技术架构设计转换为高质量的可执行代码，确保代码的企业级标准和生产部署就绪。

### 🎯 核心职责
- **代码生成**: 基于架构设计生成完整的项目代码
- **分层实现**: 严格按照分层架构实现代码结构
- **质量保证**: 集成单元测试和代码规范检查
- **性能优化**: 实现高性能和可扩展的代码解决方案

---

## 🔄 处理流程

### 📊 输入格式
```yaml
输入类型: L2层技术架构设计结果
结构:
  selected_experts: "选定的专家角色列表"
  system_architecture: "系统架构设计"
  tech_stack: "确定的技术栈"
  data_architecture: "数据架构设计"
  api_specification: "API接口规范"
  deployment_architecture: "部署架构规划"
```

### ⚡ 处理逻辑
```python
class CodeImplementation:
    def __init__(self):
        self.expert_invoker = ExpertInvoker()
        self.code_generators = {
            'java_backend': JavaBackendGenerator(),
            'react_frontend': ReactFrontendGenerator(),
            'android_mobile': AndroidGenerator(),
            'solidity_web3': SolidityGenerator()
        }
        self.quality_checker = CodeQualityChecker()
    
    def implement_code(self, l2_output):
        """L3层代码实现处理"""
        # 步骤1: 专家角色调用
        expert_responses = self.invoke_experts(l2_output)
        
        # 步骤2: 项目结构生成
        project_structure = self.generate_project_structure(l2_output, expert_responses)
        
        # 步骤3: 核心代码实现
        core_implementation = self.implement_core_code(l2_output, expert_responses)
        
        # 步骤4: 测试代码生成
        test_implementation = self.generate_test_code(core_implementation)
        
        # 步骤5: 配置文件生成
        configuration_files = self.generate_configuration(l2_output)
        
        # 步骤6: 构建脚本生成
        build_scripts = self.generate_build_scripts(l2_output)
        
        # 步骤7: 代码质量检查
        quality_report = self.quality_checker.check_code_quality(core_implementation)
        
        return {
            'project_structure': project_structure,
            'core_implementation': core_implementation,
            'test_implementation': test_implementation,
            'configuration_files': configuration_files,
            'build_scripts': build_scripts,
            'quality_report': quality_report
        }
```

---

## 🧠 专家角色调用策略

### 🎭 Java后台专家调用
```yaml
调用条件: selected_experts包含java_backend
专家路径: /rules/back/java-expert.md
调用提示词:
  角色: Java后台开发专家
  任务: 基于架构设计实现企业级Java后台代码
  输入: 
    架构设计: {system_architecture}
    技术栈: {tech_stack}
    数据设计: {data_architecture}
    API规范: {api_specification}
  要求:
    1. 严格实现分层架构 (Controller-Service-Repository-Entity)
    2. 正确应用设计模式 (工厂模式/策略模式/单例模式等)
    3. 实现完整的CRUD操作和业务逻辑
    4. 集成Spring Security安全框架
    5. 添加完整的单元测试 (覆盖率>80%)
    6. 实现异常处理和参数验证
    7. 添加接口文档注解和日志记录
    8. 实现缓存策略和性能优化
  输出: 完整的Spring Boot项目代码

期望输出结构:
  src/main/java/com/project/
  ├── controller/          # REST API控制器
  ├── service/            # 业务逻辑服务层
  ├── repository/         # 数据访问层
  ├── entity/             # 实体类
  ├── dto/                # 数据传输对象
  ├── config/             # 配置类
  ├── security/           # 安全配置
  ├── exception/          # 异常处理
  └── util/               # 工具类
```

### 🎨 React前端专家调用
```yaml
调用条件: selected_experts包含react_frontend
专家路径: /rules/front/react-expert.md
调用提示词:
  角色: React开发专家
  任务: 基于架构设计实现企业级React前端代码
  输入:
    架构设计: {system_architecture}
    技术栈: {tech_stack}
    API规范: {api_specification}
    用户场景: {user_scenarios}
  要求:
    1. 实现组件化架构 (原子/分子/组织/模板/页面)
    2. 配置状态管理 (Redux Toolkit/Zustand)
    3. 实现路由管理和代码分割
    4. 集成UI组件库和主题系统
    5. 实现API调用和错误处理
    6. 添加单元测试和集成测试
    7. 实现性能优化 (懒加载/缓存/CDN)
    8. 配置构建和部署脚本
  输出: 完整的React项目代码

期望输出结构:
  src/
  ├── components/         # 通用组件
  ├── pages/             # 页面组件
  ├── hooks/             # 自定义Hooks
  ├── store/             # 状态管理
  ├── services/          # API服务
  ├── utils/             # 工具函数
  ├── types/             # TypeScript类型
  └── styles/            # 样式文件
```

### 📱 Android专家调用
```yaml
调用条件: selected_experts包含android_mobile
专家路径: /rules/android/android-expert.md
调用提示词:
  角色: Android开发专家
  任务: 基于架构设计实现企业级Android应用代码
  输入:
    架构设计: {system_architecture}
    技术栈: {tech_stack}
    API规范: {api_specification}
    用户场景: {user_scenarios}
  要求:
    1. 实现MVVM架构模式
    2. 使用Jetpack组件 (Navigation/LiveData/ViewModel/Room)
    3. 实现网络请求和数据缓存 (Retrofit/OkHttp)
    4. 添加依赖注入 (Hilt/Dagger2)
    5. 实现UI组件和自定义View
    6. 添加单元测试和UI测试
    7. 实现性能优化和内存管理
    8. 配置混淆和签名
  输出: 完整的Android Studio项目

期望输出结构:
  app/src/main/java/com/project/
  ├── ui/                # UI层 (Activity/Fragment/ViewModel)
  ├── data/              # 数据层 (Repository/Database/Network)
  ├── domain/            # 业务逻辑层 (UseCase/Model)
  ├── di/                # 依赖注入
  └── util/              # 工具类
```

---

## 🏗️ 代码生成模板

### ☕ Java后台代码模板

#### 📋 Controller层模板
```java
package com.project.controller;

import com.project.dto.UserCreateRequest;
import com.project.dto.UserResponse;
import com.project.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

/**
 * 用户管理控制器
 * 实现用户的CRUD操作和权限控制
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
@Tag(name = "用户管理", description = "用户相关API接口")
public class UserController {

    private final UserService userService;

    @PostMapping
    @Operation(summary = "创建用户", description = "创建新的用户账号")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<UserResponse>> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        log.info("创建用户请求: {}", request.getUsername());
        
        UserResponse user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(user));
    }

    @GetMapping("/{id}")
    @Operation(summary = "获取用户详情", description = "根据用户ID获取用户信息")
    @PreAuthorize("hasRole('ADMIN') or authentication.name == #id.toString()")
    public ResponseEntity<ApiResponse<UserResponse>> getUserById(
            @PathVariable Long id) {
        log.info("获取用户详情: {}", id);
        
        UserResponse user = userService.getUserById(id);
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    @GetMapping
    @Operation(summary = "分页查询用户", description = "分页获取用户列表")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Page<UserResponse>>> getUsers(
            Pageable pageable,
            @RequestParam(required = false) String keyword) {
        log.info("分页查询用户: page={}, size={}, keyword={}", 
                pageable.getPageNumber(), pageable.getPageSize(), keyword);
        
        Page<UserResponse> users = userService.getUsers(pageable, keyword);
        return ResponseEntity.ok(ApiResponse.success(users));
    }
}
```

#### 🏢 Service层模板
```java
package com.project.service;

import com.project.dto.UserCreateRequest;
import com.project.dto.UserResponse;
import com.project.entity.User;
import com.project.exception.BusinessException;
import com.project.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户业务服务层
 * 实现用户相关的业务逻辑
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final UserMapper userMapper;

    public UserResponse createUser(UserCreateRequest request) {
        // 业务逻辑验证
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new BusinessException("用户名已存在");
        }
        
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException("邮箱已存在");
        }

        // 创建用户实体
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .passwordHash(passwordEncoder.encode(request.getPassword()))
                .status(UserStatus.ACTIVE)
                .build();

        // 保存用户
        User savedUser = userRepository.save(user);
        log.info("用户创建成功: {}", savedUser.getId());

        return userMapper.toResponse(savedUser);
    }

    @Cacheable(value = "users", key = "#id")
    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException("用户不存在"));
        
        return userMapper.toResponse(user);
    }

    @Transactional(readOnly = true)
    public Page<UserResponse> getUsers(Pageable pageable, String keyword) {
        Page<User> users;
        if (keyword != null && !keyword.trim().isEmpty()) {
            users = userRepository.findByUsernameContainingOrEmailContaining(
                    keyword, keyword, pageable);
        } else {
            users = userRepository.findAll(pageable);
        }

        return users.map(userMapper::toResponse);
    }
}
```

#### 🗄️ Repository层模板
```java
package com.project.repository;

import com.project.entity.User;
import com.project.enums.UserStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 用户数据访问层
 * 定义用户数据库操作接口
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * 根据用户名查找用户
     */
    Optional<User> findByUsername(String username);

    /**
     * 根据邮箱查找用户
     */
    Optional<User> findByEmail(String email);

    /**
     * 检查用户名是否存在
     */
    boolean existsByUsername(String username);

    /**
     * 检查邮箱是否存在
     */
    boolean existsByEmail(String email);

    /**
     * 根据状态查找用户
     */
    Page<User> findByStatus(UserStatus status, Pageable pageable);

    /**
     * 模糊查询用户名或邮箱
     */
    Page<User> findByUsernameContainingOrEmailContaining(
            String username, String email, Pageable pageable);

    /**
     * 自定义查询：获取活跃用户数量
     */
    @Query("SELECT COUNT(u) FROM User u WHERE u.status = :status")
    long countByStatus(@Param("status") UserStatus status);
}
```

### ⚛️ React前端代码模板

#### 🧩 组件模板
```typescript
// src/components/UserList/UserList.tsx
import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Input, message, Modal } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useUserStore } from '@/store/userStore';
import { User, CreateUserRequest } from '@/types/user';
import UserForm from './UserForm';
import './UserList.scss';

const { Search } = Input;

interface UserListProps {
  className?: string;
}

/**
 * 用户列表组件
 * 实现用户的增删改查操作
 */
const UserList: React.FC<UserListProps> = ({ className }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [searchKeyword, setSearchKeyword] = useState('');

  const {
    users,
    loading,
    pagination,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser
  } = useUserStore();

  useEffect(() => {
    fetchUsers({ page: 0, size: 10 });
  }, [fetchUsers]);

  const handleSearch = (value: string) => {
    setSearchKeyword(value);
    fetchUsers({ page: 0, size: 10, keyword: value });
  };

  const handleCreate = () => {
    setEditingUser(null);
    setIsModalVisible(true);
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setIsModalVisible(true);
  };

  const handleDelete = (userId: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该用户吗？',
      onOk: async () => {
        try {
          await deleteUser(userId);
          message.success('删除成功');
          fetchUsers({ page: 0, size: 10, keyword: searchKeyword });
        } catch (error) {
          message.error('删除失败');
        }
      }
    });
  };

  const handleFormSubmit = async (values: CreateUserRequest) => {
    try {
      if (editingUser) {
        await updateUser(editingUser.id, values);
        message.success('更新成功');
      } else {
        await createUser(values);
        message.success('创建成功');
      }
      setIsModalVisible(false);
      fetchUsers({ page: 0, size: 10, keyword: searchKeyword });
    } catch (error) {
      message.error(editingUser ? '更新失败' : '创建失败');
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username'
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email'
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <span className={`status-${status.toLowerCase()}`}>
          {status === 'ACTIVE' ? '活跃' : '禁用'}
        </span>
      )
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (date: string) => new Date(date).toLocaleString()
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record: User) => (
        <Space>
          <Button 
            type="link" 
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button 
            type="link" 
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      )
    }
  ];

  return (
    <div className={`user-list ${className || ''}`}>
      <div className="user-list__header">
        <h2>用户管理</h2>
        <Space>
          <Search
            placeholder="搜索用户名或邮箱"
            allowClear
            onSearch={handleSearch}
            style={{ width: 300 }}
          />
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleCreate}
          >
            新建用户
          </Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={users}
        loading={loading}
        rowKey="id"
        pagination={{
          current: pagination.page + 1,
          pageSize: pagination.size,
          total: pagination.total,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total) => `共 ${total} 条记录`
        }}
        onChange={(paginationInfo) => {
          fetchUsers({
            page: (paginationInfo.current || 1) - 1,
            size: paginationInfo.pageSize || 10,
            keyword: searchKeyword
          });
        }}
      />

      <Modal
        title={editingUser ? '编辑用户' : '新建用户'}
        visible={isModalVisible}
        footer={null}
        onCancel={() => setIsModalVisible(false)}
      >
        <UserForm
          initialValues={editingUser}
          onSubmit={handleFormSubmit}
          onCancel={() => setIsModalVisible(false)}
        />
      </Modal>
    </div>
  );
};

export default UserList;
```

#### 🏪 状态管理模板
```typescript
// src/store/userStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { userService } from '@/services/userService';
import { User, CreateUserRequest, UpdateUserRequest, UserListParams } from '@/types/user';

interface Pagination {
  page: number;
  size: number;
  total: number;
}

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
  pagination: Pagination;
}

interface UserActions {
  fetchUsers: (params: UserListParams) => Promise<void>;
  createUser: (userData: CreateUserRequest) => Promise<void>;
  updateUser: (id: number, userData: UpdateUserRequest) => Promise<void>;
  deleteUser: (id: number) => Promise<void>;
  clearError: () => void;
}

type UserStore = UserState & UserActions;

/**
 * 用户状态管理Store
 * 使用Zustand管理用户相关状态
 */
export const useUserStore = create<UserStore>()(
  devtools(
    (set, get) => ({
      // 初始状态
      users: [],
      loading: false,
      error: null,
      pagination: {
        page: 0,
        size: 10,
        total: 0
      },

      // 获取用户列表
      fetchUsers: async (params) => {
        set({ loading: true, error: null });
        try {
          const response = await userService.getUsers(params);
          set({
            users: response.data.content,
            pagination: {
              page: response.data.number,
              size: response.data.size,
              total: response.data.totalElements
            },
            loading: false
          });
        } catch (error) {
          set({ 
            loading: false, 
            error: error instanceof Error ? error.message : '获取用户列表失败' 
          });
        }
      },

      // 创建用户
      createUser: async (userData) => {
        set({ loading: true, error: null });
        try {
          await userService.createUser(userData);
          set({ loading: false });
        } catch (error) {
          set({ 
            loading: false, 
            error: error instanceof Error ? error.message : '创建用户失败' 
          });
          throw error;
        }
      },

      // 更新用户
      updateUser: async (id, userData) => {
        set({ loading: true, error: null });
        try {
          await userService.updateUser(id, userData);
          set({ loading: false });
        } catch (error) {
          set({ 
            loading: false, 
            error: error instanceof Error ? error.message : '更新用户失败' 
          });
          throw error;
        }
      },

      // 删除用户
      deleteUser: async (id) => {
        set({ loading: true, error: null });
        try {
          await userService.deleteUser(id);
          set({ loading: false });
        } catch (error) {
          set({ 
            loading: false, 
            error: error instanceof Error ? error.message : '删除用户失败' 
          });
          throw error;
        }
      },

      // 清除错误
      clearError: () => set({ error: null })
    }),
    {
      name: 'user-store'
    }
  )
);
```

---

## 🧪 测试代码生成

### ☕ Java单元测试模板
```java
package com.project.service;

import com.project.dto.UserCreateRequest;
import com.project.dto.UserResponse;
import com.project.entity.User;
import com.project.exception.BusinessException;
import com.project.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * UserService单元测试
 * 测试用户服务的核心业务逻辑
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("用户服务测试")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    private UserCreateRequest createRequest;
    private User user;
    private UserResponse userResponse;

    @BeforeEach
    void setUp() {
        createRequest = UserCreateRequest.builder()
                .username("testuser")
                .email("test@example.com")
                .password("password123")
                .build();

        user = User.builder()
                .id(1L)
                .username("testuser")
                .email("test@example.com")
                .passwordHash("hashedPassword")
                .status(UserStatus.ACTIVE)
                .build();

        userResponse = UserResponse.builder()
                .id(1L)
                .username("testuser")
                .email("test@example.com")
                .status(UserStatus.ACTIVE)
                .build();
    }

    @Test
    @DisplayName("创建用户 - 成功")
    void createUser_Success() {
        // Given
        when(userRepository.existsByUsername(createRequest.getUsername())).thenReturn(false);
        when(userRepository.existsByEmail(createRequest.getEmail())).thenReturn(false);
        when(passwordEncoder.encode(createRequest.getPassword())).thenReturn("hashedPassword");
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        // When
        UserResponse result = userService.createUser(createRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).isEqualTo("testuser");
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        
        verify(userRepository).existsByUsername("testuser");
        verify(userRepository).existsByEmail("test@example.com");
        verify(passwordEncoder).encode("password123");
        verify(userRepository).save(any(User.class));
        verify(userMapper).toResponse(user);
    }

    @Test
    @DisplayName("创建用户 - 用户名已存在")
    void createUser_UsernameExists() {
        // Given
        when(userRepository.existsByUsername(createRequest.getUsername())).thenReturn(true);

        // When & Then
        assertThatThrownBy(() -> userService.createUser(createRequest))
                .isInstanceOf(BusinessException.class)
                .hasMessage("用户名已存在");

        verify(userRepository).existsByUsername("testuser");
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("获取用户 - 成功")
    void getUserById_Success() {
        // Given
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        // When
        UserResponse result = userService.getUserById(1L);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getUsername()).isEqualTo("testuser");

        verify(userRepository).findById(1L);
        verify(userMapper).toResponse(user);
    }

    @Test
    @DisplayName("获取用户 - 用户不存在")
    void getUserById_UserNotFound() {
        // Given
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> userService.getUserById(1L))
                .isInstanceOf(BusinessException.class)
                .hasMessage("用户不存在");

        verify(userRepository).findById(1L);
        verify(userMapper, never()).toResponse(any(User.class));
    }
}
```

### ⚛️ React测试模板
```typescript
// src/components/UserList/UserList.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import UserList from './UserList';
import { useUserStore } from '@/store/userStore';

// Mock Zustand store
jest.mock('@/store/userStore');
const mockUseUserStore = useUserStore as jest.MockedFunction<typeof useUserStore>;

// Mock Ant Design message
jest.mock('antd', () => ({
  ...jest.requireActual('antd'),
  message: {
    success: jest.fn(),
    error: jest.fn()
  }
}));

const mockUsers = [
  {
    id: 1,
    username: 'testuser1',
    email: 'test1@example.com',
    status: 'ACTIVE',
    createdAt: '2024-01-01T00:00:00Z'
  },
  {
    id: 2,
    username: 'testuser2',
    email: 'test2@example.com',
    status: 'INACTIVE',
    createdAt: '2024-01-02T00:00:00Z'
  }
];

const mockUserStore = {
  users: mockUsers,
  loading: false,
  pagination: {
    page: 0,
    size: 10,
    total: 2
  },
  fetchUsers: jest.fn(),
  createUser: jest.fn(),
  updateUser: jest.fn(),
  deleteUser: jest.fn()
};

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('UserList Component', () => {
  beforeEach(() => {
    mockUseUserStore.mockReturnValue(mockUserStore);
    jest.clearAllMocks();
  });

  it('renders user list correctly', () => {
    renderWithRouter(<UserList />);
    
    expect(screen.getByText('用户管理')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('搜索用户名或邮箱')).toBeInTheDocument();
    expect(screen.getByText('新建用户')).toBeInTheDocument();
    
    // Check if users are displayed
    expect(screen.getByText('testuser1')).toBeInTheDocument();
    expect(screen.getByText('test1@example.com')).toBeInTheDocument();
    expect(screen.getByText('testuser2')).toBeInTheDocument();
    expect(screen.getByText('test2@example.com')).toBeInTheDocument();
  });

  it('calls fetchUsers on component mount', () => {
    renderWithRouter(<UserList />);
    
    expect(mockUserStore.fetchUsers).toHaveBeenCalledWith({
      page: 0,
      size: 10
    });
  });

  it('handles search functionality', async () => {
    renderWithRouter(<UserList />);
    
    const searchInput = screen.getByPlaceholderText('搜索用户名或邮箱');
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.pressEnter(searchInput);

    await waitFor(() => {
      expect(mockUserStore.fetchUsers).toHaveBeenCalledWith({
        page: 0,
        size: 10,
        keyword: 'test'
      });
    });
  });

  it('opens create user modal when new button is clicked', () => {
    renderWithRouter(<UserList />);
    
    const newUserButton = screen.getByText('新建用户');
    fireEvent.click(newUserButton);

    expect(screen.getByText('新建用户')).toBeInTheDocument();
  });

  it('handles delete user confirmation', async () => {
    renderWithRouter(<UserList />);
    
    const deleteButtons = screen.getAllByText('删除');
    fireEvent.click(deleteButtons[0]);

    expect(screen.getByText('确认删除')).toBeInTheDocument();
    expect(screen.getByText('确定要删除该用户吗？')).toBeInTheDocument();

    const confirmButton = screen.getByText('确定');
    fireEvent.click(confirmButton);

    await waitFor(() => {
      expect(mockUserStore.deleteUser).toHaveBeenCalledWith(1);
    });
  });

  it('shows loading state', () => {
    mockUseUserStore.mockReturnValue({
      ...mockUserStore,
      loading: true
    });

    renderWithRouter(<UserList />);
    
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
});
```

---

## ⚙️ 配置文件生成

### 🔧 Spring Boot配置
```yaml
# application.yml
spring:
  application:
    name: enterprise-crm-system
  
  profiles:
    active: dev
  
  datasource:
    url: jdbc:mysql://localhost:3306/crm_db?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:password}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      auto-commit: true
      idle-timeout: 300000
      pool-name: HikariCP
      max-lifetime: 1200000
      connection-timeout: 30000
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true
        use_sql_comments: false
  
  redis:
    host: ${REDIS_HOST:localhost}
    port: ${REDIS_PORT:6379}
    password: ${REDIS_PASSWORD:}
    database: 0
    timeout: 3000ms
    lettuce:
      pool:
        max-active: 8
        max-wait: -1ms
        max-idle: 8
        min-idle: 0
  
  cache:
    type: redis
    redis:
      time-to-live: 3600000
      cache-null-values: false
  
  security:
    jwt:
      secret: ${JWT_SECRET:mySecretKey}
      expiration: 86400000
      refresh-expiration: 604800000

server:
  port: 8080
  servlet:
    context-path: /api
  tomcat:
    uri-encoding: UTF-8
    max-threads: 200
    accept-count: 100

logging:
  level:
    com.project: DEBUG
    org.springframework.security: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/application.log
    max-size: 100MB
    max-history: 30

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true

springdoc:
  api-docs:
    enabled: true
    path: /v3/api-docs
  swagger-ui:
    enabled: true
    path: /swagger-ui.html
    operations-sorter: method
```

### 📦 前端构建配置
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@store': resolve(__dirname, 'src/store'),
      '@services': resolve(__dirname, 'src/services'),
      '@types': resolve(__dirname, 'src/types')
    }
  },
  
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },
  
  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: '[ext]/[name]-[hash].[ext]',
        manualChunks: {
          vendor: ['react', 'react-dom'],
          antd: ['antd'],
          utils: ['lodash', 'dayjs']
        }
      }
    }
  },
  
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false
      }
    }
  }
});
```

---

## ✅ L3层质量检查

### 🔍 代码质量标准
```yaml
代码结构检查:
  ✅ 分层架构严格实现 (Controller-Service-Repository-Entity)
  ✅ 包结构规范 (按功能模块和层次组织)
  ✅ 类命名规范 (Controller/Service/Repository后缀)
  ✅ 方法命名清晰 (动词开头，驼峰命名)

代码规范检查:
  ✅ 代码格式统一 (IDE格式化标准)
  ✅ 注释完整 (类注释/方法注释/关键逻辑注释)
  ✅ 异常处理完善 (自定义异常/统一异常处理)
  ✅ 日志记录规范 (关键操作日志/错误日志)

功能实现检查:
  ✅ CRUD操作完整 (增删改查基础功能)
  ✅ 参数验证完善 (@Valid注解/自定义验证)
  ✅ 权限控制实现 (Spring Security集成)
  ✅ 事务管理正确 (@Transactional注解使用)

性能优化检查:
  ✅ 数据库查询优化 (索引使用/分页查询)
  ✅ 缓存策略实现 (Redis缓存/本地缓存)
  ✅ 连接池配置 (HikariCP配置优化)
  ✅ 静态资源优化 (CDN/Gzip压缩)

测试覆盖检查:
  ✅ 单元测试覆盖率 (>80%覆盖率)
  ✅ 集成测试完整 (API接口测试)
  ✅ 边界情况测试 (异常情况/空值处理)
  ✅ 性能测试基准 (响应时间/并发测试)
```

---

**⚙️ L3代码实现模块通过调用专业专家和严格的代码生成标准，确保输出企业级高质量代码，为L4层质量保证提供可靠的代码基础。**