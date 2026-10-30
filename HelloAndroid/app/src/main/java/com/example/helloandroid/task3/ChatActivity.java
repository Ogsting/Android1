package com.example.helloandroid.task3;

import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.ArrayList;
import java.util.List;

/**
 * 任务 3-3：简易聊天室界面。
 * 三段式：顶部标题栏 + 中部消息列表（左右气泡）+ 底部输入框与发送按钮。
 */
public class ChatActivity extends AppCompatActivity {

    /** 消息模型：content 内容，fromMe 是否我发出的（决定气泡靠左还是靠右）。 */
    static class Msg {
        final String content;
        final boolean fromMe;

        Msg(String content, boolean fromMe) {
            this.content = content;
            this.fromMe = fromMe;
        }
    }

    private final List<Msg> messages = new ArrayList<>();
    private ChatAdapter adapter;
    private EditText etInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        etInput = findViewById(R.id.et_chat_input);
        RecyclerView rv = findViewById(R.id.rv_chat);
        rv.setLayoutManager(new LinearLayoutManager(this));

        messages.add(new Msg("你好，我是 AI 助手", false));
        messages.add(new Msg("你好，我在做实验一", true));

        adapter = new ChatAdapter(messages);
        rv.setAdapter(adapter);

        Button btnSend = findViewById(R.id.btn_chat_send);
        btnSend.setOnClickListener(v -> {
            String text = etInput.getText().toString().trim();
            if (TextUtils.isEmpty(text)) {
                Toast.makeText(this, "不能发送空消息", Toast.LENGTH_SHORT).show();
                return;
            }
            messages.add(new Msg(text, true));
            adapter.notifyItemInserted(messages.size() - 1);
            etInput.setText("");
            // 滚动到底部，模拟真实聊天的体验
            rv.scrollToPosition(messages.size() - 1);
        });
    }
}
