package com.example.helloandroid.task3;

import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;

/**
 * 任务 3-1：四种基础布局与常用控件综合练习。
 * <p>
 * 布局：根布局 LinearLayout（垂直 + layout_weight 均分），内部嵌套 RelativeLayout / FrameLayout，
 * 表单区域使用 ConstraintLayout，覆盖指导书要求的四种布局。
 * 控件：TextView / EditText / Button / ImageView / RadioButton / CheckBox / Switch。
 */
public class LoginActivity extends AppCompatActivity {

    private EditText etUsername;
    private EditText etPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);

        Button btnLogin = findViewById(R.id.btn_login);
        btnLogin.setOnClickListener(v -> {
            // trim() 去掉用户可能误输入的首尾空格，避免"看似输入了却校验失败"
            String username = etUsername.getText().toString().trim();
            String password = etPassword.getText().toString().trim();

            if (TextUtils.isEmpty(username)) {
                Toast.makeText(this, "用户名不能为空", Toast.LENGTH_SHORT).show();
                return;
            }
            if (TextUtils.isEmpty(password)) {
                Toast.makeText(this, "密码不能为空", Toast.LENGTH_SHORT).show();
                return;
            }

            RadioGroup rgRole = findViewById(R.id.rg_role);
            CheckBox cbRemember = findViewById(R.id.cb_remember);
            Switch swNotify = findViewById(R.id.sw_notify);

            StringBuilder sb = new StringBuilder();
            sb.append("登录成功：").append(username);
            sb.append("\n角色：").append(rgRole.getCheckedRadioButtonId() == R.id.rb_teacher ? "教师" : "学生");
            sb.append("\n记住密码：").append(cbRemember.isChecked());
            sb.append("\n接收通知：").append(swNotify.isChecked());

            Toast.makeText(this, sb.toString(), Toast.LENGTH_LONG).show();
        });

        // 注册按钮：清空表单，演示控件赋值（setText）
        Button btnRegister = findViewById(R.id.btn_register);
        btnRegister.setOnClickListener(v -> {
            etUsername.setText("");
            etPassword.setText("");
            etUsername.requestFocus();
            Toast.makeText(this, "已清空表单", Toast.LENGTH_SHORT).show();
        });
    }
}
