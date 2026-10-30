package com.example.lab;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 实验一 任务 7 / 任务 9 后端启动类。
 * <p>
 * Spring Boot 内置 Tomcat，启动后监听 8080 端口，
 * 模拟器通过 http://10.0.2.2:8080 访问宿主机。
 */
@SpringBootApplication
@MapperScan("com.example.lab.mapper")
public class LabServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(LabServerApplication.class, args);
    }
}
