package com.example.helloandroid.broadcast;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

/** 任务 4：有序广播接收器 B（优先级 50，后收到）。 */
public class OrderedReceiverB extends BroadcastReceiver {

    private static final String TAG = "OrderedReceiverB";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.i(TAG, "收到有序广播，优先级 50，内容："
                + intent.getStringExtra("msg") + "，上一个接收器结果：" + getResultData());
    }
}
