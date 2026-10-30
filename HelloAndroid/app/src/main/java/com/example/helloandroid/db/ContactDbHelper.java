package com.example.helloandroid.db;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

/**
 * 任务 5-2：SQLite 数据库帮助类。
 * <p>
 * onCreate 只在数据库文件第一次创建时执行一次；
 * 修改表结构必须提升 VERSION，让 onUpgrade 生效，否则改动不会应用。
 */
public class ContactDbHelper extends SQLiteOpenHelper {

    public static final String DB_NAME = "contact.db";
    /** 版本号从 1 升到 2，用于演示 onUpgrade 增加 gender 列。 */
    public static final int VERSION = 2;

    public ContactDbHelper(Context context) {
        super(context, DB_NAME, null, VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE contact(" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "name TEXT NOT NULL," +
                "phone TEXT," +
                "email TEXT)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        if (oldVersion < 2) {
            // 增量升级：只加列，不丢数据
            db.execSQL("ALTER TABLE contact ADD COLUMN gender TEXT");
        }
    }
}
