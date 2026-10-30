package com.example.helloandroid.service;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

/**
 * 任务 8：后台服务演示。
 * <p>
 * 同一个 Service 同时支持两种启动方式：
 * · startService()  启动式：onCreate → onStartCommand，与调用方无关联，需 stopService 停止；
 * · bindService()   绑定式：onCreate → onBind，调用方可拿到 Binder 直接调用方法，解绑后销毁。
 */
public class MyService extends Service {

    private static final String TAG = "MyService";

    private int counter = 0;

    /** 供绑定方直接调用的 Binder 实现。 */
    public class LocalBinder extends Binder {
        public MyService getService() {
            return MyService.this;
        }
    }

    private final IBinder binder = new LocalBinder();

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "onCreate：服务创建");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "onStartCommand：startId = " + startId);
        // START_STICKY：服务被系统杀死后尝试重建
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        Log.d(TAG, "onBind：有客户端绑定");
        return binder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        Log.d(TAG, "onUnbind：客户端解绑");
        return super.onUnbind(intent);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy：服务销毁");
    }

    /** 绑定式调用的业务方法，用于验证 Activity 与服务确实通信成功。 */
    public int increase() {
        return ++counter;
    }
}
