package com.example.helloandroid.permission;

import android.Manifest;
import android.content.ContentResolver;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.example.helloandroid.R;

/**
 * 任务 6-1：运行时权限 + ContentResolver 读取系统通讯录。
 * <p>
 * READ_CONTACTS 属于危险权限，必须在运行时动态申请；
 * 未授予时调用 ContentResolver 会抛 SecurityException。
 */
public class PermissionContactActivity extends AppCompatActivity {

    private static final String TAG = "PermissionContact";
    private static final int REQ_READ_CONTACTS = 1;

    private TextView tvResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_permission_contact);
        tvResult = findViewById(R.id.tv_permission_result);

        Button btnRead = findViewById(R.id.btn_read_contacts);
        btnRead.setOnClickListener(v -> checkAndRead());

        Button btnQueryProvider = findViewById(R.id.btn_query_provider);
        // 通过 ContentResolver 访问本应用自定义的 ContentProvider（任务 6-3）
        btnQueryProvider.setOnClickListener(v -> queryOwnProvider());
    }

    /** 先检查再申请，这是 Android 6.0 之后的固定套路。 */
    private void checkAndRead() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)
                != PackageManager.PERMISSION_GRANTED) {
            // 未授权：发起申请，结果回到 onRequestPermissionsResult
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.READ_CONTACTS}, REQ_READ_CONTACTS);
        } else {
            readContacts();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ_READ_CONTACTS) {
            // grantResults 可能为空（用户直接取消），必须判空
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                readContacts();
            } else {
                Toast.makeText(this, "权限被拒绝，无法读取通讯录", Toast.LENGTH_SHORT).show();
            }
        }
    }

    /** 通过 ContentResolver 查询系统通讯录，取前 10 条显示。 */
    private void readContacts() {
        StringBuilder sb = new StringBuilder("系统通讯录（前 10 条）：\n");
        // 投影只取需要的列，减少开销；Cursor 用 try-with-resources 自动关闭
        try (Cursor cursor = getContentResolver().query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                new String[]{ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
                        ContactsContract.CommonDataKinds.Phone.NUMBER},
                null, null,
                ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME + " ASC")) {
            if (cursor == null) {
                sb.append("查询返回空");
            } else {
                int count = 0;
                while (cursor.moveToNext() && count < 10) {
                    String name = cursor.getString(0);
                    String number = cursor.getString(1);
                    sb.append(name).append(" : ").append(number).append('\n');
                    count++;
                }
                if (count == 0) {
                    sb.append("（模拟器通讯录为空，请先在通讯录 App 中添加联系人）");
                }
            }
        } catch (Exception e) {
            sb.append("读取失败：").append(e.getMessage());
            Log.e(TAG, "readContacts error", e);
        }
        tvResult.setText(sb.toString());
    }

    /** 访问本应用自定义 ContentProvider，验证 provider 注册是否生效。 */
    private void queryOwnProvider() {
        StringBuilder sb = new StringBuilder("自定义 ContentProvider 数据：\n");
        ContentResolver resolver = getContentResolver();
        try (Cursor cursor = resolver.query(
                ContactProvider.CONTENT_URI, null, null, null, "id DESC")) {
            if (cursor == null || cursor.getCount() == 0) {
                sb.append("（暂无数据，请先到任务5-2 添加联系人）");
            } else {
                while (cursor.moveToNext()) {
                    sb.append(cursor.getString(cursor.getColumnIndexOrThrow("name")))
                            .append(" : ")
                            .append(cursor.getString(cursor.getColumnIndexOrThrow("phone")))
                            .append('\n');
                }
            }
        } catch (Exception e) {
            sb.append("访问失败：").append(e.getMessage());
            Log.e(TAG, "queryOwnProvider error", e);
        }
        tvResult.setText(sb.toString());
    }
}
