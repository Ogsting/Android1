package com.example.helloandroid.task3;

import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.List;

/**
 * 任务 3-3：聊天消息适配器。
 * 通过判断 fromMe 动态设置气泡所在侧与背景色，实现左右气泡区分。
 */
public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.VH> {

    private final List<ChatActivity.Msg> data;

    public ChatAdapter(List<ChatActivity.Msg> data) {
        this.data = data;
    }

    public static class VH extends RecyclerView.ViewHolder {
        final LinearLayout row;
        final TextView bubble;

        public VH(@NonNull View itemView) {
            super(itemView);
            row = itemView.findViewById(R.id.ll_chat_row);
            bubble = itemView.findViewById(R.id.tv_chat_bubble);
        }
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_chat, parent, false);
        return new VH(v);
    }

    @Override
    public void onBindViewHolder(@NonNull VH holder, int position) {
        ChatActivity.Msg msg = data.get(position);
        holder.bubble.setText(msg.content);

        if (msg.fromMe) {
            // 我方消息靠右，蓝色气泡
            holder.row.setGravity(Gravity.END);
            holder.bubble.setBackgroundColor(0xFF3F51B5);
            holder.bubble.setTextColor(0xFFFFFFFF);
        } else {
            // 对方消息靠左，灰色气泡
            holder.row.setGravity(Gravity.START);
            holder.bubble.setBackgroundColor(0xFFE0E0E0);
            holder.bubble.setTextColor(0xFF222222);
        }
    }

    @Override
    public int getItemCount() {
        return data.size();
    }
}
