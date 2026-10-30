package com.example.helloandroid.db;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.ArrayList;
import java.util.List;

/**
 * 任务 5-2：SQLite 通讯录案例。
 * 支持新增、按姓名模糊查询、点击编辑、长按删除，并演示批量插入事务。
 */
public class DbContactActivity extends AppCompatActivity {

    private ContactDao dao;
    private DbContactAdapter adapter;
    private final List<Contact> data = new ArrayList<>();

    private EditText etName;
    private EditText etPhone;
    private EditText etEmail;
    private EditText etKeyword;
    /** 当前正在编辑的联系人 id，-1 表示新增模式。 */
    private long editingId = -1L;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_db_contact);

        dao = new ContactDao(this);
        etName = findViewById(R.id.et_name);
        etPhone = findViewById(R.id.et_phone);
        etEmail = findViewById(R.id.et_email);
        etKeyword = findViewById(R.id.et_keyword);

        RecyclerView rv = findViewById(R.id.rv_db_contacts);
        rv.setLayoutManager(new LinearLayoutManager(this));
        adapter = new DbContactAdapter(data, new DbContactAdapter.Listener() {
            @Override
            public void onEdit(Contact contact) {
                // 点击把数据回填到表单，进入编辑模式
                editingId = contact.getId();
                etName.setText(contact.getName());
                etPhone.setText(contact.getPhone());
                etEmail.setText(contact.getEmail());
                Toast.makeText(DbContactActivity.this, "编辑模式，修改后点保存", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onDelete(Contact contact) {
                new AlertDialog.Builder(DbContactActivity.this)
                        .setTitle("删除确认")
                        .setMessage("确定删除 " + contact.getName() + " 吗？")
                        .setPositiveButton("删除", (d, w) -> {
                            dao.delete(contact.getId());
                            reload(etKeyword.getText().toString());
                        })
                        .setNegativeButton("取消", null)
                        .show();
            }
        });
        rv.setAdapter(adapter);

        // 保存（新增或修改）
        Button btnSave = findViewById(R.id.btn_save);
        btnSave.setOnClickListener(v -> saveContact());

        // 模糊查询
        findViewById(R.id.btn_search).setOnClickListener(v -> reload(etKeyword.getText().toString()));

        // 显示全部
        findViewById(R.id.btn_show_all).setOnClickListener(v -> {
            etKeyword.setText("");
            reload("");
        });

        // 批量插入（事务演示）
        findViewById(R.id.btn_batch).setOnClickListener(v -> {
            List<Contact> batch = new ArrayList<>();
            batch.add(new Contact("事务A", "13900000001", "a@lab.com"));
            batch.add(new Contact("事务B", "13900000002", "b@lab.com"));
            batch.add(new Contact("事务C", "13900000003", "c@lab.com"));
            dao.insertBatch(batch);
            Toast.makeText(this, "事务批量插入 3 条完成", Toast.LENGTH_SHORT).show();
            reload("");
        });

        TextView tvDbPath = findViewById(R.id.tv_db_path);
        tvDbPath.setText("数据库路径：" + getDatabasePath(ContactDbHelper.DB_NAME).getAbsolutePath());

        reload("");
    }

    /** 根据 editingId 决定执行 insert 还是 update。 */
    private void saveContact() {
        String name = etName.getText().toString().trim();
        String phone = etPhone.getText().toString().trim();
        String email = etEmail.getText().toString().trim();

        if (name.isEmpty()) {
            Toast.makeText(this, "姓名不能为空", Toast.LENGTH_SHORT).show();
            return;
        }

        Contact c = new Contact(name, phone, email);
        if (editingId > 0) {
            c.setId(editingId);
            dao.update(c);
            Toast.makeText(this, "已更新", Toast.LENGTH_SHORT).show();
            editingId = -1L;
        } else {
            dao.insert(c);
            Toast.makeText(this, "已新增", Toast.LENGTH_SHORT).show();
        }

        etName.setText("");
        etPhone.setText("");
        etEmail.setText("");
        reload(etKeyword.getText().toString());
    }

    /** 重新查询并刷新列表。 */
    private void reload(String keyword) {
        data.clear();
        data.addAll(dao.query(keyword));
        adapter.notifyDataSetChanged();
    }
}
