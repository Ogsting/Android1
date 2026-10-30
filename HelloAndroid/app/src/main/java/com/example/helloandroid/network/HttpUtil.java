package com.example.helloandroid.network;

import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/**
 * 任务 7：通用网络请求工具类。
 * <p>
 * 统一封装四件事：
 * 1) 在子线程发起请求（Android 禁止主线程网络操作）；
 * 2) 设置连接/读取超时，避免无限等待；
 * 3) 用 Handler 切回主线程回调，调用方可以直接更新 UI；
 * 4) 异常统一处理，回调 onError 而不是让线程静默崩溃。
 */
public final class HttpUtil {

    private static final String TAG = "HttpUtil";

    /** 主线程 Handler，用于把结果切回 UI 线程。 */
    private static final Handler MAIN = new Handler(Looper.getMainLooper());

    public interface Callback {
        void onSuccess(String json);

        void onError(String message);
    }

    private HttpUtil() {
    }

    /** 发起 GET 请求。 */
    public static void get(String url, Callback callback) {
        request("GET", url, null, callback);
    }

    /** 发起 POST 请求，body 为 JSON 字符串。 */
    public static void post(String url, String jsonBody, Callback callback) {
        request("POST", url, jsonBody, callback);
    }

    /** 发起 PUT 请求，用于任务 9 的修改员工。 */
    public static void put(String url, String jsonBody, Callback callback) {
        request("PUT", url, jsonBody, callback);
    }

    /** 发起 DELETE 请求。 */
    public static void delete(String url, Callback callback) {
        request("DELETE", url, null, callback);
    }

    private static void request(final String method, final String url,
                                final String jsonBody, final Callback callback) {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                conn = (HttpURLConnection) new URL(url).openConnection();
                conn.setRequestMethod(method);
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                // 声明请求体为 JSON，否则后端可能返回 415
                conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                conn.setRequestProperty("Accept", "application/json");

                if (jsonBody != null) {
                    conn.setDoOutput(true);
                    try (OutputStream os = conn.getOutputStream()) {
                        os.write(jsonBody.getBytes(StandardCharsets.UTF_8));
                    }
                }

                int code = conn.getResponseCode();
                InputStream is = (code >= 200 && code < 300)
                        ? conn.getInputStream() : conn.getErrorStream();
                String body = readAll(is);
                Log.i(TAG, method + " " + url + " -> " + code + " : " + body);

                if (code >= 200 && code < 300) {
                    final String result = body;
                    MAIN.post(() -> callback.onSuccess(result));
                } else {
                    final String err = "HTTP " + code + "：" + body;
                    MAIN.post(() -> callback.onError(err));
                }
            } catch (Exception e) {
                Log.e(TAG, method + " " + url + " 失败", e);
                final String msg = e.getClass().getSimpleName() + "：" + e.getMessage();
                MAIN.post(() -> callback.onError(msg));
            } finally {
                if (conn != null) {
                    conn.disconnect();
                }
            }
        }).start();
    }

    private static String readAll(InputStream is) throws Exception {
        if (is == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(is, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
        }
        return sb.toString();
    }
}
