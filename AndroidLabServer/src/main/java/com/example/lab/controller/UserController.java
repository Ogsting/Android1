package com.example.lab.controller;

import com.example.lab.entity.User;
import com.example.lab.mapper.UserMapper;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 任务 7：用户接口。
 * 刻意返回裸 JSON 数组（而不是统一包装），用于让客户端对比
 * org.json 的 JSONArray 解析与 Gson 的 List&lt;User&gt; 解析。
 */
@RestController
@RequestMapping("/api")
public class UserController {

    private final UserMapper userMapper;

    public UserController(UserMapper userMapper) {
        this.userMapper = userMapper;
    }

    @GetMapping("/users")
    public List<User> list() {
        return userMapper.findAll();
    }

    @PostMapping("/users")
    public User add(@RequestBody User user) {
        userMapper.insert(user);
        // insert 后 id 已被 MyBatis 回填，直接返回完整对象
        return user;
    }
}
