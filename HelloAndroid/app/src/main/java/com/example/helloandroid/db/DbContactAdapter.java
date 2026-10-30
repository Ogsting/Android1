package com.example.helloandroid.db;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.List;

/** 任务 5-2：通讯录列表适配器，支持点击编辑与长按删除。 */
public class DbContactAdapter extends RecyclerView.Adapter<DbContactAdapter.VH> {

    public interface Listener {
        void onEdit(Contact contact);

        void onDelete(Contact contact);
    }

    private final List<Contact> data;
    private final Listener listener;

    public DbContactAdapter(List<Contact> data, Listener listener) {
        this.data = data;
        this.listener = listener;
    }

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
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_contact, parent, false);
        return new VH(v);
    }

    @Override
    public void onBindViewHolder(@NonNull VH holder, int position) {
        Contact c = data.get(position);
        holder.tvName.setText(c.getName());
        holder.tvPhone.setText(c.getPhone() + "  " + (c.getEmail() == null ? "" : c.getEmail()));

        holder.itemView.setOnClickListener(v -> {
            if (listener != null) {
                listener.onEdit(c);
            }
        });
        holder.itemView.setOnLongClickListener(v -> {
            if (listener != null) {
                listener.onDelete(c);
            }
            return true;
        });
    }

    @Override
    public int getItemCount() {
        return data.size();
    }
}
