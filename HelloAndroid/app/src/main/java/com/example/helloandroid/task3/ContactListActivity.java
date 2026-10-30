package com.example.helloandroid.task3;

import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.ArrayList;
import java.util.List;

/**
 * 任务 3-2：RecyclerView 联系人列表。
 * 三步固定流程：setLayoutManager → setAdapter → 提供数据源。
 */
public class ContactListActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact_list);

        RecyclerView rv = findViewById(R.id.rv_contacts);
        // 1. 设置布局管理器，决定子项排布方式
        rv.setLayoutManager(new LinearLayoutManager(this));

        // 2. 准备模拟数据源
        List<Contact> data = new ArrayList<>();
        data.add(new Contact("张三", "13800000001"));
        data.add(new Contact("李四", "13800000002"));
        data.add(new Contact("王五", "13800000003"));
        data.add(new Contact("赵六", "13800000004"));
        data.add(new Contact("孙七", "13800000005"));
        data.add(new Contact("周八", "13800000006"));

        // 3. 设置适配器，并把点击事件通过回调抛给 Activity 处理
        ContactAdapter adapter = new ContactAdapter(data,
                contact -> Toast.makeText(this, "点击了 " + contact.getName(), Toast.LENGTH_SHORT).show());
        rv.setAdapter(adapter);
    }
}
