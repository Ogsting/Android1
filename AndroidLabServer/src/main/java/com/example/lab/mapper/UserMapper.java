package com.example.lab.mapper;

import com.example.lab.entity.User;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/** 任务 7：用户表数据访问接口，SQL 写在 resources/mapper/UserMapper.xml。 */
@Mapper
public interface UserMapper {

    List<User> findAll();

    User findById(Long id);

    int insert(User user);
}
