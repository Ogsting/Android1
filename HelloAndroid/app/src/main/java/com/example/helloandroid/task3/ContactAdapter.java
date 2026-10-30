package com.example.helloandroid.task3;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.List;

/**
 * 任务 3-2：RecyclerView 适配器。
 * <p>
 * 与 ListView 的 BaseAdapter + convertView 复用相比，RecyclerView 强制使用 ViewHolder，
 * 把 findViewById 的结果缓存起来，滚动时不再重复查找控件。
 */
public class ContactAdapter extends RecyclerView.Adapter<ContactAdapter.VH> {

    /** 回调接口：把点击事件交给外部处理，适配器只负责展示。 */
    public interface OnItemClickListener {
        void onItemClick(Contact contact);
    }

    private final List<Contact> data;
    private final OnItemClickListener listener;

    public ContactAdapter(List<Contact> data, OnItemClickListener listener) {
        this.data = data;
        this.listener = listener;
    }

    /** ViewHolder：持有子项内部控件引用，避免重复 findViewById。 */
    public static class VH extends RecyclerView.ViewHolder {
        final TextView tvName;
        final TextView tvPhone;

        public VH(@NonNull View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tv_name);
            tvPhone = itemView.findViewById(R.id.tv_phone);
        }
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // inflate 的第三个参数必须为 false，否则子项会丢失父布局的 LayoutParams
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_contact, parent, false);
        return new VH(v);
    }

    @Override
    public void onBindViewHolder(@NonNull VH holder, int position) {
        Contact c = data.get(position);
        holder.tvName.setText(c.getName());
        holder.tvPhone.setText(c.getPhone());
        holder.itemView.setOnClickListener(v -> {
            if (listener != null) {
                listener.onItemClick(c);
            }
        });
    }

    @Override
    public int getItemCount() {
        return data.size();
    }
}
