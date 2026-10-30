package com.example.helloandroid.emp;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.helloandroid.R;

import java.util.List;

/** 任务 9：员工列表适配器。 */
public class EmpAdapter extends RecyclerView.Adapter<EmpAdapter.VH> {

    public interface Listener {
        void onEdit(Emp emp);

        void onDelete(Emp emp);
    }

    private final List<Emp> data;
    private final Listener listener;

    public EmpAdapter(List<Emp> data, Listener listener) {
        this.data = data;
        this.listener = listener;
    }

    public static class VH extends RecyclerView.ViewHolder {
        final TextView tvName;
        final TextView tvDept;
        final TextView tvPost;
        final TextView tvSalary;

        public VH(@NonNull View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tv_emp_name);
            tvDept = itemView.findViewById(R.id.tv_emp_dept);
            tvPost = itemView.findViewById(R.id.tv_emp_post);
            tvSalary = itemView.findViewById(R.id.tv_emp_salary);
        }
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_emp, parent, false);
        return new VH(v);
    }

    @Override
    public void onBindViewHolder(@NonNull VH holder, int position) {
        Emp e = data.get(position);
        holder.tvName.setText(e.getEmpName() + "（ID " + e.getEmpId() + "）");
        holder.tvDept.setText("部门：" + (e.getDept() == null ? "-" : e.getDept()));
        holder.tvPost.setText("岗位：" + (e.getPost() == null ? "-" : e.getPost()));
        holder.tvSalary.setText("薪资：" + e.getSalary());

        holder.itemView.setOnClickListener(v -> {
            if (listener != null) {
                listener.onEdit(e);
            }
        });
        holder.itemView.setOnLongClickListener(v -> {
            if (listener != null) {
                listener.onDelete(e);
            }
            return true;
        });
    }

    @Override
    public int getItemCount() {
        return data.size();
    }
}
