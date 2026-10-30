package com.example.helloandroid.service;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

/**
 * 任务 8-1：Service 生命周期演示。
 * 通过日志对比"启动式"与"绑定式"两种方式触发的回调差异。
 */
public class ServiceActivity extends AppCompatActivity {

    private static final String TAG = "ServiceActivity";

    private MyService boundService;
    private boolean isBound = false;
    private TextView tvStatus;

    /** ServiceConnection 回调运行在主线程，拿到 Binder 后即可强转并调用服务方法。 */
    private final ServiceConnection connection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            MyService.LocalBinder binder = (MyService.LocalBinder) service;
            boundService = binder.getService();
            isBound = true;
            tvStatus.append("\n绑定成功，调用服务方法 increase() = " + boundService.increase());
            Log.i(TAG, "onServiceConnected");
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            isBound = false;
            boundService = null;
            Log.i(TAG, "onServiceDisconnected");
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_service);
        tvStatus = findViewById(R.id.tv_service_status);

        // 启动式
        Button btnStart = findViewById(R.id.btn_start_service);
        btnStart.setOnClickListener(v -> {
            startService(new Intent(this, MyService.class));
            tvStatus.append("\nstartService() 已调用");
        });

        Button btnStop = findViewById(R.id.btn_stop_service);
        btnStop.setOnClickListener(v -> {
            stopService(new Intent(this, MyService.class));
            tvStatus.append("\nstopService() 已调用");
        });

        // 绑定式
        Button btnBind = findViewById(R.id.btn_bind_service);
        btnBind.setOnClickListener(v -> {
            if (!isBound) {
                bindService(new Intent(this, MyService.class), connection, Context.BIND_AUTO_CREATE);
            }
        });

        Button btnUnbind = findViewById(R.id.btn_unbind_service);
        btnUnbind.setOnClickListener(v -> {
            if (isBound) {
                unbindService(connection);
                isBound = false;
                tvStatus.append("\nunbindService() 已调用");
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 必须解绑，否则抛 ServiceConnection 泄漏异常
        if (isBound) {
            unbindService(connection);
            isBound = false;
        }
    }
}
