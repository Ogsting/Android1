-- ============================================================
-- 实验一 任务 7 / 任务 9 数据库初始化脚本
-- 数据库：android_lab（结构与先修课 ssm_emp.emp 保持一致）
-- 字符集：utf8mb4，避免中文乱码
-- ============================================================

CREATE DATABASE IF NOT EXISTS android_lab
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE android_lab;

-- 任务 7：演示用用户表
DROP TABLE IF EXISTS t_user;
CREATE TABLE t_user (
    id       BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
    username VARCHAR(50)  NOT NULL COMMENT '登录名',
    nickname VARCHAR(50)  DEFAULT NULL COMMENT '昵称',
    age      INT          DEFAULT NULL COMMENT '年龄',
    email    VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT ='用户表';

INSERT INTO t_user (username, nickname, age, email) VALUES
('zhangsan', '张三', 20, 'zhangsan@example.com'),
('lisi',     '李四', 21, 'lisi@example.com'),
('wangwu',   '王五', 22, 'wangwu@example.com'),
('zhaoliu',  '赵六', 23, 'zhaoliu@example.com');

-- 任务 9：员工表（照搬 ssm_emp.emp 结构，字段含义一致）
DROP TABLE IF EXISTS emp;
CREATE TABLE emp (
    emp_id    INT          NOT NULL AUTO_INCREMENT COMMENT '员工编号',
    emp_name  VARCHAR(50)  NOT NULL COMMENT '姓名',
    gender    CHAR(1)      DEFAULT '男' COMMENT '性别',
    dept      VARCHAR(50)  DEFAULT NULL COMMENT '部门',
    post      VARCHAR(50)  DEFAULT NULL COMMENT '岗位',
    salary    DECIMAL(10,2) DEFAULT NULL COMMENT '薪资',
    hire_date DATE         DEFAULT NULL COMMENT '入职时间',
    status    TINYINT      DEFAULT 1 COMMENT '状态：1在职 0离职',
    PRIMARY KEY (emp_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT ='员工表';

INSERT INTO emp (emp_name, gender, dept, post, salary, hire_date, status) VALUES
('张伟',  '男', '研发部', 'Java开发工程师', 12000.00, '2024-07-01', 1),
('李娜',  '女', '研发部', '前端工程师',     10000.00, '2024-08-15', 1),
('王强',  '男', '市场部', '市场专员',        8000.00, '2023-03-10', 1),
('刘敏',  '女', '人事部', '人事专员',        7500.00, '2022-06-20', 0),
('陈晨',  '男', '测试部', '测试员',          6000.00, '2026-10-23', 1),
('赵磊',  '男', '研发部', 'Android开发工程师', 11000.00, '2025-01-06', 1),
('孙悦',  '女', '运营部', '运营专员',        6800.00, '2025-09-01', 1);

SELECT '初始化完成' AS result,
       (SELECT COUNT(*) FROM t_user) AS user_count,
       (SELECT COUNT(*) FROM emp) AS emp_count;
