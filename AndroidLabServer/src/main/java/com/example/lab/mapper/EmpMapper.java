package com.example.lab.mapper;

import com.example.lab.entity.Emp;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/** 任务 9：员工表数据访问接口。 */
@Mapper
public interface EmpMapper {

    /** 分页查询：limit/offset 由 Service 计算后传入。 */
    List<Emp> findPage(@Param("offset") int offset, @Param("size") int size);

    long count();

    Emp findById(Integer empId);

    int insert(Emp emp);

    int update(Emp emp);

    int deleteById(Integer empId);
}
