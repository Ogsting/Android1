package com.example.helloandroid.task2;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

/**
 * 任务 2：SecondActivity，负责接收 FirstActivity 传来的 Bundle 数据并回传结果。
 * <p>
 * 启动模式由 AndroidManifest.xml 中的 android:launchMode 控制，
 * 通过反复跳转并在日志中打印 taskId 可观察任务栈中实例数量的变化。
 */
public class SecondActivity extends AppCompatActivity {

    private static final String TAG = "SecondActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        Log.d(TAG, "onCreate");

        // 接收上一个页面通过 Intent 传来的参数
        Intent intent = getIntent();
        String username = intent.getStringExtra("username");
        int age = intent.getIntExtra("age", -1);
        boolean isVip = intent.getBooleanExtra("isVip", false);

        TextView tvInfo = findViewById(R.id.tv_params);
        tvInfo.setText("username = " + username + "\nage = " + age + "\nisVip = " + isVip);

        // 再开一个 SecondActivity 自身，用于观察四种启动模式下实例数量差异
        Button btnSelf = findViewById(R.id.btn_self);
        btnSelf.setOnClickListener(v -> {
            startActivity(new Intent(SecondActivity.this, SecondActivity.class));
            Log.d(TAG, "taskId = " + getTaskId() + ", 当前实例 hashCode = " + hashCode());
        });

        // 回传结果并结束当前页面
        Button btnBack = findViewById(R.id.btn_reply);
        btnBack.setOnClickListener(v -> {
            Intent reply = new Intent();
            reply.putExtra("result", "欢迎 " + username);
            setResult(RESULT_OK, reply);
            finish();
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG, "onPause");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d(TAG, "onStop");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy");
    }
}
