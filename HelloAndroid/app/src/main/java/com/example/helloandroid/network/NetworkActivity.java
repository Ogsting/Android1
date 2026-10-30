package com.example.helloandroid.network;

import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.helloandroid.R;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.json.JSONArray;
import org.json.JSONObject;

import java.lang.reflect.Type;
import java.util.List;

/**
 * 任务 7：网络请求 + JSON 解析。
 * <p>
 * 分别用 org.json 与 Gson 解析同一份后端数据，对比两种方式的差异：
 * · org.json：Android 内置，逐字段手工取值，无需额外依赖，适合结构简单的场景；
 * · Gson：反射自动映射实体类，代码量少，适合结构复杂的场景，需要引入依赖。
 */
public class NetworkActivity extends AppCompatActivity {

    private static final String TAG = "NetworkActivity";

    private TextView tvResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_network);
        tvResult = findViewById(R.id.tv_network_result);

        // 1) GET + org.json 解析
        Button btnOrgJson = findViewById(R.id.btn_get_orgjson);
        btnOrgJson.setOnClickListener(v -> HttpUtil.get(ApiConfig.BASE_URL + "/api/users",
                new HttpUtil.Callback() {
                    @Override
                    public void onSuccess(String json) {
                        parseWithOrgJson(json);
                    }

                    @Override
                    public void onError(String message) {
                        tvResult.setText("请求失败：" + message
                                + "\n请确认后端已启动，且使用 10.0.2.2 访问宿主机。");
                    }
                }));

        // 2) GET + Gson 解析
        Button btnGson = findViewById(R.id.btn_get_gson);
        btnGson.setOnClickListener(v -> HttpUtil.get(ApiConfig.BASE_URL + "/api/users",
                new HttpUtil.Callback() {
                    @Override
                    public void onSuccess(String json) {
                        parseWithGson(json);
                    }

                    @Override
                    public void onError(String message) {
                        tvResult.setText("请求失败：" + message);
                    }
                }));

        // 3) POST 提交 JSON
        Button btnPost = findViewById(R.id.btn_post_user);
        btnPost.setOnClickListener(v -> {
            User u = new User();
            u.setUsername("lab" + System.currentTimeMillis() % 1000);
            u.setNickname("实验新增用户");
            u.setAge(22);
            u.setEmail("lab@example.com");
            String body = new Gson().toJson(u);
            HttpUtil.post(ApiConfig.BASE_URL + "/api/users", body, new HttpUtil.Callback() {
                @Override
                public void onSuccess(String json) {
                    tvResult.setText("POST 成功，服务端返回：\n" + json);
                }

                @Override
                public void onError(String message) {
                    tvResult.setText("POST 失败：" + message);
                }
            });
        });
    }

    /** 用 Android 内置的 org.json 逐字段解析。 */
    private void parseWithOrgJson(String json) {
        StringBuilder sb = new StringBuilder("org.json 解析结果：\n");
        try {
            JSONArray array = new JSONArray(json);
            for (int i = 0; i < array.length(); i++) {
                JSONObject o = array.getJSONObject(i);
                sb.append(o.getLong("id")).append(". ")
                        .append(o.optString("nickname"))
                        .append("（").append(o.optString("username")).append("）")
                        .append('\n');
            }
            sb.append("\n共 ").append(array.length()).append(" 条");
        } catch (Exception e) {
            sb.append("解析异常：").append(e.getMessage());
            Log.e(TAG, "parseWithOrgJson", e);
        }
        tvResult.setText(sb.toString());
    }

    /** 用 Gson 的 TypeToken 反序列化为 List<User>。 */
    private void parseWithGson(String json) {
        StringBuilder sb = new StringBuilder("Gson 解析结果：\n");
        try {
            Type type = new TypeToken<List<User>>() {
            }.getType();
            List<User> users = new Gson().fromJson(json, type);
            for (User u : users) {
                sb.append(u.toString()).append('\n');
            }
            sb.append("\n共 ").append(users.size()).append(" 条");
        } catch (Exception e) {
            sb.append("解析异常：").append(e.getMessage());
            Log.e(TAG, "parseWithGson", e);
        }
        tvResult.setText(sb.toString());
    }
}
