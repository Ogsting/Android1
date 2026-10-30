package com.example.helloandroid.permission;

import android.content.ContentProvider;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.net.Uri;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.helloandroid.db.ContactDbHelper;

/**
 * 任务 6-3：自定义 ContentProvider，把任务 5 的通讯录数据对外共享。
 * <p>
 * ContentProvider 相比直接暴露数据库文件的好处：
 * 1) 统一 URI 访问入口，调用方不需要知道底层是 SQLite 还是文件；
 * 2) 可配合 readPermission / writePermission 做细粒度权限管控；
 * 3) 跨进程访问由系统 Binder 机制保证，无需自行处理 IPC。
 */
public class ContactProvider extends ContentProvider {

    /** authority 必须与 AndroidManifest.xml 中 android:authorities 完全一致。 */
    public static final String AUTHORITY = "com.example.helloandroid.provider";
    public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/contact");

    private static final int CODE_CONTACT_DIR = 0;
    private static final int CODE_CONTACT_ITEM = 1;
    private static final UriMatcher MATCHER = new UriMatcher(UriMatcher.NO_MATCH);

    static {
        // content://authority/contact      → 整个表
        MATCHER.addURI(AUTHORITY, "contact", CODE_CONTACT_DIR);
        // content://authority/contact/12   → 单条记录
        MATCHER.addURI(AUTHORITY, "contact/#", CODE_CONTACT_ITEM);
    }

    private ContactDbHelper helper;

    @Override
    public boolean onCreate() {
        helper = new ContactDbHelper(getContext());
        return helper != null;
    }

    @Nullable
    @Override
    public Cursor query(@NonNull Uri uri, @Nullable String[] projection, @Nullable String selection,
                        @Nullable String[] selectionArgs, @Nullable String sortOrder) {
        SQLiteDatabase db = helper.getReadableDatabase();
        Cursor cursor;
        switch (MATCHER.match(uri)) {
            case CODE_CONTACT_DIR:
                cursor = db.query("contact", projection, selection, selectionArgs,
                        null, null, sortOrder);
                break;
            case CODE_CONTACT_ITEM:
                // 用路径段拼出 id 条件，仍然走参数化查询
                String id = uri.getPathSegments().get(1);
                cursor = db.query("contact", projection, "id = ?", new String[]{id},
                        null, null, sortOrder);
                break;
            default:
                throw new IllegalArgumentException("未知 URI: " + uri);
        }
        // 通知监听该 URI 的观察者（ContentObserver）
        if (getContext() != null) {
            cursor.setNotificationUri(getContext().getContentResolver(), uri);
        }
        return cursor;
    }

    @Nullable
    @Override
    public Uri insert(@NonNull Uri uri, @Nullable ContentValues values) {
        SQLiteDatabase db = helper.getWritableDatabase();
        long id = db.insert("contact", null, values);
        if (id > 0 && getContext() != null) {
            getContext().getContentResolver().notifyChange(uri, null);
        }
        // 返回带新 id 的完整 URI
        return ContentUris.withAppendedId(CONTENT_URI, id);
    }

    @Override
    public int update(@NonNull Uri uri, @Nullable ContentValues values,
                      @Nullable String selection, @Nullable String[] selectionArgs) {
        SQLiteDatabase db = helper.getWritableDatabase();
        int rows;
        if (MATCHER.match(uri) == CODE_CONTACT_ITEM) {
            String id = uri.getPathSegments().get(1);
            rows = db.update("contact", values, "id = ?", new String[]{id});
        } else {
            rows = db.update("contact", values, selection, selectionArgs);
        }
        if (getContext() != null) {
            getContext().getContentResolver().notifyChange(uri, null);
        }
        return rows;
    }

    @Override
    public int delete(@NonNull Uri uri, @Nullable String selection, @Nullable String[] selectionArgs) {
        SQLiteDatabase db = helper.getWritableDatabase();
        int rows;
        if (MATCHER.match(uri) == CODE_CONTACT_ITEM) {
            String id = uri.getPathSegments().get(1);
            rows = db.delete("contact", "id = ?", new String[]{id});
        } else {
            rows = db.delete("contact", selection, selectionArgs);
        }
        if (getContext() != null) {
            getContext().getContentResolver().notifyChange(uri, null);
        }
        return rows;
    }

    @Nullable
    @Override
    public String getType(@NonNull Uri uri) {
        // MIME 类型：dir 用 vnd.android.cursor.dir，item 用 vnd.android.cursor.item
        switch (MATCHER.match(uri)) {
            case CODE_CONTACT_DIR:
                return "vnd.android.cursor.dir/vnd." + AUTHORITY + ".contact";
            case CODE_CONTACT_ITEM:
                return "vnd.android.cursor.item/vnd." + AUTHORITY + ".contact";
            default:
                return null;
        }
    }
}
