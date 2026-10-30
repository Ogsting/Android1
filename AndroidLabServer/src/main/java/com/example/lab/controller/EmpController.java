package com.example.lab.controller;

import com.example.lab.common.Result;
import com.example.lab.entity.Emp;
import com.example.lab.service.EmpService;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 任务 9：员工管理 REST 接口。
 * <p>
 * GET    /api/emps?page=1&size=5   分页列表
 * GET    /api/emp/{id}             单个员工
 * POST   /api/emp                  新增
 * PUT    /api/emp                  修改
 * DELETE /api/emp/{id}             删除
 */
@RestController
@RequestMapping("/api")
public class EmpController {

    private final EmpService empService;

    public EmpController(EmpService empService) {
        this.empService = empService;
    }

    @GetMapping("/emps")
    public Map<String, Object> page(@RequestParam(defaultValue = "1") int page,
                                    @RequestParam(defaultValue = "5") int size) {
        // 直接返回 {total,page,size,list}，与客户端 EmpListActivity 的解析结构一致
        return empService.page(page, size);
    }

    @GetMapping("/emp/{id}")
    public Result<Emp> detail(@PathVariable Integer id) {
        Emp emp = empService.findById(id);
        return emp == null ? Result.fail("员工不存在") : Result.ok(emp);
    }

    @PostMapping("/emp")
    public Result<Void> add(@RequestBody Emp emp) {
        try {
            empService.insert(emp);
            return Result.ok();
        } catch (Exception e) {
            return Result.fail("新增失败：" + e.getMessage());
        }
    }

    @PutMapping("/emp")
    public Result<Void> update(@RequestBody Emp emp) {
        try {
            empService.update(emp);
            return Result.ok();
        } catch (Exception e) {
            return Result.fail("修改失败：" + e.getMessage());
        }
    }

    @DeleteMapping("/emp/{id}")
    public Result<Void> delete(@PathVariable Integer id) {
        try {
            empService.delete(id);
            return Result.ok();
        } catch (Exception e) {
            return Result.fail("删除失败：" + e.getMessage());
        }
    }
}
