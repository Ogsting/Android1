package com.example.helloandroid.emp;

import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;
import com.example.helloandroid.network.ApiConfig;
import com.example.helloandroid.network.HttpUtil;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

/**
 * 任务 9：Android 客户端与 SpringMVC 后端整合（员工管理 CRUD）。
 * <p>
 * 涉及：分页加载、POST 新增、PUT 修改、DELETE 删除、加载状态与异常提示。
 * 接口契约：
 * GET    /api/emps?page=1&size=5  → {"total":7,"list":[...]}
 * POST   /api/emp                 → {"code":0,"msg":"success"}
 * PUT    /api/emp                 → {"code":0,"msg":"success"}
 * DELETE /api/emp/{id}            → {"code":0,"msg":"success"}
 */
public class EmpListActivity extends AppCompatActivity {

    private static final String TAG = "EmpListActivity";

    private final List<Emp> data = new ArrayList<>();
    private EmpAdapter adapter;
    private TextView tvStatus;
    private EditText etName;
    private EditText etDept;
    private EditText etPost;
    private EditText etSalary;

    /** 当前页码，从 1 开始。 */
    private int page = 1;
    private int total = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emp);

        tvStatus = findViewById(R.id.tv_emp_status);
        etName = findViewById(R.id.et_emp_name);
        etDept = findViewById(R.id.et_emp_dept);
        etPost = findViewById(R.id.et_emp_post);
        etSalary = findViewById(R.id.et_emp_salary);

        RecyclerView rv = findViewById(R.id.rv_emps);
        rv.setLayoutManager(new LinearLayoutManager(this));
        adapter = new EmpAdapter(data, new EmpAdapter.Listener() {
            @Override
            public void onEdit(Emp emp) {
                showEditDialog(emp);
            }

            @Override
            public void onDelete(Emp emp) {
                new AlertDialog.Builder(EmpListActivity.this)
                        .setTitle("删除确认")
                        .setMessage("确定删除员工 " + emp.getEmpName() + " 吗？")
                        .setPositiveButton("删除", (d, w) -> deleteEmp(emp))
                        .setNegativeButton("取消", null)
                        .show();
            }
        });
        rv.setAdapter(adapter);

        // 新增员工
        Button btnAdd = findViewById(R.id.btn_emp_add);
        btnAdd.setOnClickListener(v -> addEmp());

        // 重新加载第一页
        findViewById(R.id.btn_emp_reload).setOnClickListener(v -> loadPage(1, true));

        // 加载下一页（触底分页）
        findViewById(R.id.btn_emp_more).setOnClickListener(v -> {
            if (data.size() >= total && total > 0) {
                Toast.makeText(this, "已加载全部 " + total + " 条", Toast.LENGTH_SHORT).show();
                return;
            }
            loadPage(page + 1, false);
        });

        loadPage(1, true);
    }

    /** 分页加载。reset=true 表示清空后重新加载第一页。 */
    private void loadPage(int targetPage, boolean reset) {
        tvStatus.setText("加载中… 第 " + targetPage + " 页");
        String url = ApiConfig.BASE_URL + "/api/emps?page=" + targetPage + "&size=" + ApiConfig.PAGE_SIZE;

        HttpUtil.get(url, new HttpUtil.Callback() {
            @Override
            public void onSuccess(String json) {
                try {
                    // 解析 {total, page, size, list}
                    JsonObject root = JsonParser.parseString(json).getAsJsonObject();
                    total = root.get("total").getAsInt();
                    Type listType = new TypeToken<List<Emp>>() {
                    }.getType();
                    List<Emp> list = new Gson().fromJson(root.get("list"), listType);

                    if (reset) {
                        data.clear();
                    }
                    if (list != null) {
                        data.addAll(list);
                    }
                    page = targetPage;
                    adapter.notifyDataSetChanged();
                    tvStatus.setText("第 " + page + " 页加载完成，共 " + total + " 条，当前显示 " + data.size() + " 条");
                } catch (Exception e) {
                    Log.e(TAG, "解析失败", e);
                    tvStatus.setText("JSON 解析失败：" + e.getMessage());
                }
            }

            @Override
            public void onError(String message) {
                tvStatus.setText("请求失败：" + message
                        + "\n请确认：后端已启动 / 使用 10.0.2.2 / 已开启明文 HTTP");
            }
        });
    }

    /** POST 新增：把表单数据序列化为 JSON 提交。 */
    private void addEmp() {
        String name = etName.getText().toString().trim();
        if (TextUtils.isEmpty(name)) {
            Toast.makeText(this, "姓名不能为空", Toast.LENGTH_SHORT).show();
            return;
        }

        Emp emp = new Emp();
        emp.setEmpName(name);
        emp.setDept(etDept.getText().toString().trim());
        emp.setPost(etPost.getText().toString().trim());
        emp.setSalary(parseSalary(etSalary.getText().toString()));
        emp.setGender("男");
        emp.setStatus(1);

        String body = new Gson().toJson(emp);
        tvStatus.setText("正在新增…");
        HttpUtil.post(ApiConfig.BASE_URL + "/api/emp", body, new HttpUtil.Callback() {
            @Override
            public void onSuccess(String json) {
                Toast.makeText(EmpListActivity.this, "新增成功", Toast.LENGTH_SHORT).show();
                etName.setText("");
                etDept.setText("");
                etPost.setText("");
                etSalary.setText("");
                loadPage(1, true);
            }

            @Override
            public void onError(String message) {
                tvStatus.setText("新增失败：" + message);
            }
        });
    }

    /** PUT 修改：弹窗修改岗位与薪资。 */
    private void showEditDialog(Emp emp) {
        EditText input = new EditText(this);
        input.setText(emp.getPost());
        input.setHint("新岗位");

        new AlertDialog.Builder(this)
                .setTitle("修改 " + emp.getEmpName() + " 的岗位")
                .setView(input)
                .setPositiveButton("保存", (d, w) -> {
                    emp.setPost(input.getText().toString().trim());
                    String body = new Gson().toJson(emp);
                    HttpUtil.put(ApiConfig.BASE_URL + "/api/emp", body, new HttpUtil.Callback() {
                        @Override
                        public void onSuccess(String json) {
                            Toast.makeText(EmpListActivity.this, "修改成功", Toast.LENGTH_SHORT).show();
                            loadPage(1, true);
                        }

                        @Override
                        public void onError(String message) {
                            tvStatus.setText("修改失败：" + message);
                        }
                    });
                })
                .setNegativeButton("取消", null)
                .show();
    }

    /** DELETE 删除。 */
    private void deleteEmp(Emp emp) {
        HttpUtil.delete(ApiConfig.BASE_URL + "/api/emp/" + emp.getEmpId(), new HttpUtil.Callback() {
            @Override
            public void onSuccess(String json) {
                Toast.makeText(EmpListActivity.this, "删除成功", Toast.LENGTH_SHORT).show();
                loadPage(1, true);
            }

            @Override
            public void onError(String message) {
                tvStatus.setText("删除失败：" + message);
            }
        });
    }

    /** 薪资输入容错：非法输入按 0 处理，避免 NumberFormatException 崩溃。 */
    private double parseSalary(String text) {
        if (TextUtils.isEmpty(text)) {
            return 0d;
        }
        try {
            return Double.parseDouble(text.trim());
        } catch (NumberFormatException e) {
            return 0d;
        }
    }
}
