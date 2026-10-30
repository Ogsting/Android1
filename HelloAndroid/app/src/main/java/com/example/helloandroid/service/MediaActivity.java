package com.example.helloandroid.service;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.example.helloandroid.R;

/**
 * 任务 8-2：定位与多媒体。
 * <p>
 * · 定位：使用系统 LocationManager 获取一次定位（无需第三方地图 Key）；
 * · 多媒体：MediaPlayer 播放网络音频，Intent 调用系统相机拍照。
 */
public class MediaActivity extends AppCompatActivity {

    private static final String TAG = "MediaActivity";
    private static final int REQ_CAMERA = 2;
    private static final int REQ_CAMERA_PERMISSION = 3;

    private MediaPlayer player;
    private TextView tvStatus;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_media);
        tvStatus = findViewById(R.id.tv_media_status);

        // ---- 定位 ----
        findViewById(R.id.btn_locate).setOnClickListener(v -> locateOnce());

        // ---- MediaPlayer 播放网络音频 ----
        Button btnPlay = findViewById(R.id.btn_play_audio);
        btnPlay.setOnClickListener(v -> {
            try {
                if (player == null) {
                    player = new MediaPlayer();
                    // 网络音频地址，需保证设备可访问互联网
                    player.setDataSource("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3");
                    // prepare() 同步准备会阻塞主线程，演示用 prepareAsync 更规范
                    player.setOnPreparedListener(mp -> {
                        mp.start();
                        tvStatus.setText("音频开始播放");
                    });
                    player.setOnErrorListener((mp, what, extra) -> {
                        tvStatus.setText("播放失败：what=" + what + ", extra=" + extra);
                        return false;
                    });
                    player.prepareAsync();
                    tvStatus.setText("正在准备音频…");
                } else {
                    // 状态机：只有在 prepared 之后才能 start
                    player.start();
                    tvStatus.setText("继续播放");
                }
            } catch (Exception e) {
                Log.e(TAG, "MediaPlayer 异常", e);
                tvStatus.setText("MediaPlayer 异常：" + e.getMessage());
            }
        });

        Button btnPause = findViewById(R.id.btn_pause_audio);
        btnPause.setOnClickListener(v -> {
            if (player != null && player.isPlaying()) {
                player.pause();
                tvStatus.setText("音频已暂停");
            }
        });

        // ---- 调用系统相机 ----
        Button btnCamera = findViewById(R.id.btn_take_photo);
        btnCamera.setOnClickListener(v -> {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.CAMERA}, REQ_CAMERA_PERMISSION);
            } else {
                openCamera();
            }
        });
    }

    private void openCamera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (intent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(intent, REQ_CAMERA);
        } else {
            Toast.makeText(this, "没有可用的相机应用", Toast.LENGTH_SHORT).show();
        }
    }

    /** 获取一次定位（需 ACCESS_FINE_LOCATION / ACCESS_COARSE_LOCATION 已授权）。 */
    private void locateOnce() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_COARSE_LOCATION,
                            Manifest.permission.ACCESS_FINE_LOCATION}, 4);
            return;
        }
        LocationManager lm = (LocationManager) getSystemService(LOCATION_SERVICE);
        try {
            // 模拟器可在 Extended controls → Location 中注入一个坐标
            Location last = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            if (last == null) {
                last = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
            }
            if (last != null) {
                tvStatus.setText("定位成功：\n纬度 " + last.getLatitude()
                        + "\n经度 " + last.getLongitude()
                        + "\n精度 " + last.getAccuracy() + " m");
            } else {
                tvStatus.setText("暂无定位缓存，请在模拟器 Extended controls → Location 注入坐标后重试");
            }
        } catch (SecurityException e) {
            tvStatus.setText("缺少定位权限：" + e.getMessage());
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ_CAMERA_PERMISSION && grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            openCamera();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // MediaPlayer 持有底层解码器资源，必须释放
        if (player != null) {
            player.release();
            player = null;
        }
    }
}
