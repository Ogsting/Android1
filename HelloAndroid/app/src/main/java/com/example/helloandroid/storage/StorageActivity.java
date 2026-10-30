package com.example.helloandroid.storage;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

/**
 * 任务 5-1：文件存储 + SharedPreferences。
 * <p>
 * 文件存储适合保存较大的、非结构化的文本/二进制数据；
 * SharedPreferences 适合保存少量键值对配置（如"记住密码"的登录信息）。
 */
public class StorageActivity extends AppCompatActivity {

    private static final String TAG = "StorageActivity";
    private static final String FILE_NAME = "note.txt";
    private static final String SP_NAME = "login_pref";

    private EditText etInput;
    private TextView tvOutput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_storage);

        etInput = findViewById(R.id.et_storage_input);
        tvOutput = findViewById(R.id.tv_storage_output);

        // ---- 文件存储：写 ----
        findViewById(R.id.btn_write_file).setOnClickListener(v -> {
            String content = etInput.getText().toString();
            try (FileOutputStream fos = openFileOutput(FILE_NAME, MODE_PRIVATE)) {
                // MODE_PRIVATE：仅本应用可读写
                fos.write(content.getBytes(StandardCharsets.UTF_8));
                Toast.makeText(this, "写入成功", Toast.LENGTH_SHORT).show();
                Log.i(TAG, "写入文件：" + getFilesDir() + "/" + FILE_NAME);
            } catch (Exception e) {
                Log.e(TAG, "写文件失败", e);
            }
        });

        // ---- 文件存储：读 ----
        findViewById(R.id.btn_read_file).setOnClickListener(v -> {
            try (FileInputStream fis = openFileInput(FILE_NAME)) {
                byte[] buf = new byte[fis.available()];
                int len = fis.read(buf);
                tvOutput.setText("文件内容：\n" + new String(buf, 0, Math.max(len, 0), StandardCharsets.UTF_8));
            } catch (Exception e) {
                tvOutput.setText("文件内容：（读取失败，" + e.getMessage() + "）");
                Log.e(TAG, "读文件失败", e);
            }
        });

        // ---- SharedPreferences：保存"记住密码" ----
        findViewById(R.id.btn_sp_save).setOnClickListener(v -> {
            SharedPreferences sp = getSharedPreferences(SP_NAME, MODE_PRIVATE);
            // apply() 异步落盘，commit() 同步返回 boolean。UI 线程推荐 apply()
            sp.edit()
                    .putString("username", etInput.getText().toString())
                    .putBoolean("remember", true)
                    .apply();
            Toast.makeText(this, "已保存到 SharedPreferences", Toast.LENGTH_SHORT).show();
        });

        // ---- SharedPreferences：读取 ----
        findViewById(R.id.btn_sp_read).setOnClickListener(v -> {
            SharedPreferences sp = getSharedPreferences(SP_NAME, MODE_PRIVATE);
            String username = sp.getString("username", "（无）");
            boolean remember = sp.getBoolean("remember", false);
            tvOutput.setText("SP 内容：\nusername = " + username + "\nremember = " + remember);
        });

        Button btnClear = findViewById(R.id.btn_sp_clear);
        btnClear.setOnClickListener(v -> {
            getSharedPreferences(SP_NAME, MODE_PRIVATE).edit().clear().apply();
            tvOutput.setText("已清空 SharedPreferences");
        });
    }
}
