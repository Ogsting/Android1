package com.example.lab.service;

import com.example.lab.entity.Emp;
import com.example.lab.mapper.EmpMapper;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 任务 9：员工业务层。
 * 分页参数在这里换算成 offset，Controller 只负责接收请求与包装响应。
 */
@Service
public class EmpService {

    private final EmpMapper empMapper;

    public EmpService(EmpMapper empMapper) {
        this.empMapper = empMapper;
    }

    public Map<String, Object> page(int page, int size) {
        // 页码与页大小做下限保护，避免负数导致 SQL 报错
        int safePage = Math.max(page, 1);
        int safeSize = Math.max(size, 1);
        int offset = (safePage - 1) * safeSize;

        List<Emp> list = empMapper.findPage(offset, safeSize);
        long total = empMapper.count();

        Map<String, Object> data = new LinkedHashMap<>();
        data.put("total", total);
        data.put("page", safePage);
        data.put("size", safeSize);
        data.put("list", list);
        return data;
    }

    public Emp findById(Integer empId) {
        return empMapper.findById(empId);
    }

    public int insert(Emp emp) {
        // 未填入职日期时按今天写入，保证 NOT NULL 之外的字段不出现空值
        if (emp.getHireDate() == null) {
            emp.setHireDate(java.time.LocalDate.now());
        }
        if (emp.getStatus() == null) {
            emp.setStatus(1);
        }
        return empMapper.insert(emp);
    }

    public int update(Emp emp) {
        if (emp.getEmpId() == null) {
            throw new IllegalArgumentException("修改必须提供 empId");
        }
        return empMapper.update(emp);
    }

    public int delete(Integer empId) {
        return empMapper.deleteById(empId);
    }
}
