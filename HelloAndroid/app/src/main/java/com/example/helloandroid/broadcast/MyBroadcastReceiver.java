package com.example.helloandroid.broadcast;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

/**
 * 任务 4：自定义广播接收器（静态注册）。
 * <p>
 * 在 AndroidManifest.xml 中通过 &lt;receiver&gt; 声明并配置 action，
 * 即使应用未启动也能被系统拉起（Android 8.0 起对隐式广播有限制）。
 */
public class MyBroadcastReceiver extends BroadcastReceiver {

    /** 自定义广播的动作字符串，发送方与接收方必须完全一致。 */
    public static final String ACTION_CUSTOM = "com.example.helloandroid.CUSTOM_BROADCAST";

    @Override
    public void onReceive(Context context, Intent intent) {
        // onReceive 运行在主线程，耗时操作必须另起线程，否则会 ANR
        String msg = intent.getStringExtra("msg");
        Toast.makeText(context, "静态接收器收到：" + msg, Toast.LENGTH_SHORT).show();
    }
}
