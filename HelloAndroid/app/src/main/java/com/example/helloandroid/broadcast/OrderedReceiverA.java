package com.example.helloandroid.broadcast;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

/**
 * 任务 4：有序广播接收器 A（优先级 100，先收到）。
 * <p>
 * 有序广播按 priority 从高到低依次投递，优先级高的接收器可以：
 * 1) 修改结果数据 setResultData；
 * 2) 调用 abortBroadcast() 截断，后续接收器将收不到。
 */
public class OrderedReceiverA extends BroadcastReceiver {

    private static final String TAG = "OrderedReceiverA";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.i(TAG, "收到有序广播，优先级 100，内容：" + intent.getStringExtra("msg"));
        // 把结果改写，供后续接收器读取
        setResultData("A 已处理");
    }
}
