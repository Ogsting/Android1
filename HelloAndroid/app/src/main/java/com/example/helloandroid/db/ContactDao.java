package com.example.helloandroid.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import java.util.ArrayList;
import java.util.List;

/**
 * 任务 5-2：通讯录 DAO（数据访问对象）。
 * <p>
 * 所有条件都用参数化（?）传入，杜绝字符串拼接造成的 SQL 注入；
 * 查询结束后 Cursor 必须关闭，否则泄漏（此处用 try-with-resources 保证）。
 */
public class ContactDao {

    private final ContactDbHelper helper;

    public ContactDao(Context context) {
        this.helper = new ContactDbHelper(context.getApplicationContext());
    }

    /** 新增：使用 ContentValues 参数化写入，自动转义。 */
    public long insert(Contact c) {
        SQLiteDatabase db = helper.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put("name", c.getName());
        cv.put("phone", c.getPhone());
        cv.put("email", c.getEmail());
        cv.put("gender", c.getGender());
        return db.insert("contact", null, cv);
    }

    /** 修改：按 id 更新指定联系人的姓名与电话。 */
    public int update(Contact c) {
        SQLiteDatabase db = helper.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put("name", c.getName());
        cv.put("phone", c.getPhone());
        cv.put("email", c.getEmail());
        return db.update("contact", cv, "id = ?", new String[]{String.valueOf(c.getId())});
    }

    /** 删除：按 id 删除。 */
    public int delete(long id) {
        SQLiteDatabase db = helper.getWritableDatabase();
        return db.delete("contact", "id = ?", new String[]{String.valueOf(id)});
    }

    /** 查询：按姓名模糊查询，关键字为空则返回全部，按 id 倒序。 */
    public List<Contact> query(String keyword) {
        SQLiteDatabase db = helper.getReadableDatabase();
        List<Contact> list = new ArrayList<>();

        String selection = null;
        String[] args = null;
        if (keyword != null && !keyword.trim().isEmpty()) {
            selection = "name LIKE ?";
            args = new String[]{"%" + keyword.trim() + "%"};
        }

        // try-with-resources 保证 Cursor 一定被关闭
        try (Cursor cursor = db.query("contact", null, selection, args,
                null, null, "id DESC")) {
            while (cursor.moveToNext()) {
                Contact c = new Contact();
                c.setId(cursor.getLong(cursor.getColumnIndexOrThrow("id")));
                c.setName(cursor.getString(cursor.getColumnIndexOrThrow("name")));
                c.setPhone(cursor.getString(cursor.getColumnIndexOrThrow("phone")));
                c.setEmail(cursor.getString(cursor.getColumnIndexOrThrow("email")));
                c.setGender(cursor.getString(cursor.getColumnIndexOrThrow("gender")));
                list.add(c);
            }
        }
        return list;
    }

    /**
     * 批量导入演示事务：要么全部成功，要么全部回滚。
     * 忘记 setTransactionSuccessful 会导致整个事务被回滚。
     */
    public void insertBatch(List<Contact> contacts) {
        SQLiteDatabase db = helper.getWritableDatabase();
        db.beginTransaction();
        try {
            for (Contact c : contacts) {
                ContentValues cv = new ContentValues();
                cv.put("name", c.getName());
                cv.put("phone", c.getPhone());
                cv.put("email", c.getEmail());
                cv.put("gender", c.getGender());
                db.insert("contact", null, cv);
            }
            // 必须调用，否则 endTransaction 时回滚全部写入
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
        }
    }
}
