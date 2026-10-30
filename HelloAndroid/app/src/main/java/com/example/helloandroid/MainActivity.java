package com.example.helloandroid;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.broadcast.BroadcastActivity;
import com.example.helloandroid.db.DbContactActivity;
import com.example.helloandroid.emp.EmpListActivity;
import com.example.helloandroid.network.NetworkActivity;
import com.example.helloandroid.permission.PermissionContactActivity;
import com.example.helloandroid.service.MediaActivity;
import com.example.helloandroid.service.ServiceActivity;
import com.example.helloandroid.storage.StorageActivity;
import com.example.helloandroid.task2.FirstActivity;
import com.example.helloandroid.task3.ChatActivity;
import com.example.helloandroid.task3.ContactListActivity;
import com.example.helloandroid.task3.LoginActivity;

/**
 * 任务 1：Android 开发环境搭建与项目基础。
 * <p>
 * 本 Activity 承担两件事：
 * 1) 在 onCreate 中输出 Log.v/d/i/w/e 五级日志，用于在 Logcat 中验证环境；
 * 2) 作为实验一的导航入口，点击按钮进入任务 2~9 的演示页面。
 */
public class MainActivity extends AppCompatActivity {

    /** Logcat 过滤标签，全大写是 Android 社区约定。 */
    private static final String TAG = "HelloAndroid";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 五级日志验证：级别由低到高 v < d < i < w < e
        Log.v(TAG, "onCreate: verbose 日志，最细粒度，仅本地调试使用");
        Log.d(TAG, "onCreate: debug 日志，开发期调试信息");
        Log.i(TAG, "onCreate: info 日志，关键流程节点");
        Log.w(TAG, "onCreate: warn 日志，潜在风险提示");
        Log.e(TAG, "onCreate: error 日志，错误但未导致崩溃");

        bindNavigation();
    }

    /** 绑定 9 个任务的入口按钮，统一用 lambda 写法避免重复的匿名内部类。 */
    private void bindNavigation() {
        bind(R.id.btn_task1, null);                       // 当前页即任务 1
        bind(R.id.btn_task2, FirstActivity.class);        // Activity 生命周期与 Intent
        bind(R.id.btn_task3_login, LoginActivity.class);  // 布局与控件：登录页
        bind(R.id.btn_task3_list, ContactListActivity.class); // RecyclerView 列表
        bind(R.id.btn_task3_chat, ChatActivity.class);    // 简易聊天室界面
        bind(R.id.btn_task4, BroadcastActivity.class);    // 广播机制
        bind(R.id.btn_task5, StorageActivity.class);      // 文件与 SharedPreferences
        bind(R.id.btn_task5_db, DbContactActivity.class); // SQLite 通讯录
        bind(R.id.btn_task6, PermissionContactActivity.class); // 权限与内容提供器
        bind(R.id.btn_task7, NetworkActivity.class);      // 网络与 JSON 解析
        bind(R.id.btn_task8, ServiceActivity.class);      // Service 生命周期
        bind(R.id.btn_task8_media, MediaActivity.class);  // 定位与多媒体
        bind(R.id.btn_task9, EmpListActivity.class);      // SpringMVC 整合案例
    }

    private void bind(int id, final Class<?> target) {
        Button button = findViewById(id);
        if (target == null) {
            button.setOnClickListener(v -> Log.i(TAG, "当前页即任务 1，无需跳转"));
            return;
        }
        button.setOnClickListener((View v) -> startActivity(new Intent(this, target)));
    }
}
