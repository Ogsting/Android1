package com.example.helloandroid.broadcast;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

/**
 * 任务 4：广播机制演示。
 * <p>
 * 1) 动态注册网络变化监听，必须在 onDestroy 中注销，否则泄漏；
 * 2) 发送自定义广播给静态注册的 MyBroadcastReceiver；
 * 3) 发送有序广播，观察 priority 决定的投递顺序。
 */
public class BroadcastActivity extends AppCompatActivity {

    private static final String TAG = "BroadcastActivity";

    private NetworkChangeReceiver networkReceiver;
    private TextView tvStatus;
    private boolean registered = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_broadcast);

        tvStatus = findViewById(R.id.tv_broadcast_status);

        // 1) 动态注册：代码中注册，生命周期随 Activity
        IntentFilter filter = new IntentFilter();
        filter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
        networkReceiver = new NetworkChangeReceiver();
        registerReceiver(networkReceiver, filter);
        registered = true;

        // 2) 发送普通自定义广播（静态接收器可收到）
        Button btnSendCustom = findViewById(R.id.btn_send_custom);
        btnSendCustom.setOnClickListener(v -> {
            Intent intent = new Intent(MyBroadcastReceiver.ACTION_CUSTOM);
            intent.setPackage(getPackageName()); // 限定本应用，规避 Android 8.0+ 隐式广播限制
            intent.putExtra("msg", "你好，静态接收器");
            sendBroadcast(intent);
            tvStatus.setText("已发送普通自定义广播");
            Log.i(TAG, "sendBroadcast: " + MyBroadcastReceiver.ACTION_CUSTOM);
        });

        // 3) 发送有序广播
        Button btnSendOrdered = findViewById(R.id.btn_send_ordered);
        btnSendOrdered.setOnClickListener(v -> {
            Intent intent = new Intent("com.example.helloandroid.ORDERED_BROADCAST");
            intent.setPackage(getPackageName());
            intent.putExtra("msg", "有序广播内容");
            sendOrderedBroadcast(intent, null);
            tvStatus.setText("已发送有序广播，请看 Logcat 中 A(100) → B(50) 的顺序");
            Log.i(TAG, "sendOrderedBroadcast 已发送");
        });
    }

    /** 内部类动态接收器：监听网络连接状态变化。 */
    class NetworkChangeReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            NetworkInfo info = cm.getActiveNetworkInfo();
            boolean online = info != null && info.isAvailable();
            String text = "网络状态变化：" + (online ? "已连接（" + info.getTypeName() + "）" : "已断开");
            tvStatus.setText(text);
            Log.i(TAG, text);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 动态注册的接收器必须注销，否则报 leaked IntentReceiver 异常
        if (registered) {
            unregisterReceiver(networkReceiver);
            registered = false;
        }
    }
}
