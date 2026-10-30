package com.example.helloandroid.task2;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

/**
 * 任务 2：Activity 生命周期 + Intent 显式跳转 / Bundle 传参 / 结果回传。
 * <p>
 * 生命周期方法全部重写并打印日志，配合按 Home 键、旋转屏幕、finish() 观察执行顺序。
 */
public class FirstActivity extends AppCompatActivity {

    private static final String TAG = "FirstActivity";

    private TextView tvLog;
    private TextView tvResult;

    /**
     * 新版结果回调 API：替代已废弃的 startActivityForResult/onActivityResult。
     * 必须在 onCreate 之前（字段初始化阶段）注册。
     */
    private final ActivityResultLauncher<Intent> secondLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    String reply = result.getData().getStringExtra("result");
                    tvResult.setText("收到回传：" + reply);
                    Log.i(TAG, "onActivityResult: " + reply);
                } else {
                    tvResult.setText("收到回传：用户取消");
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first);
        Log.d(TAG, "onCreate");
        tvLog = findViewById(R.id.tv_lifecycle_log);
        tvResult = findViewById(R.id.tv_result);

        Button btnJump = findViewById(R.id.btn_jump);
        btnJump.setOnClickListener(v -> {
            // 显式 Intent：明确指定目标组件
            Intent intent = new Intent(FirstActivity.this, SecondActivity.class);
            intent.putExtra("username", "张三");
            intent.putExtra("age", 20);
            intent.putExtra("isVip", true);
            // 使用 launcher 启动才能拿到回传结果
            secondLauncher.launch(intent);
        });

        Button btnBrowser = findViewById(R.id.btn_implicit);
        // 隐式 Intent：只声明动作，由系统匹配能处理该动作的应用
        btnBrowser.setOnClickListener(v -> {
            Intent implicit = new Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://www.android.com"));
            startActivity(implicit);
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart");
        append("onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume");
        append("onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG, "onPause");
        append("onPause");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d(TAG, "onStop");
        append("onStop");
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Log.d(TAG, "onRestart");
        append("onRestart");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy");
    }

    /** 把生命周期回调追加显示在界面上，方便截图说明执行顺序。 */
    private void append(String name) {
        if (tvLog != null) {
            tvLog.append(name + " → ");
        }
    }
}
