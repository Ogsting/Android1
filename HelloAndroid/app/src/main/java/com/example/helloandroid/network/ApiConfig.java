package com.example.helloandroid.network;

/**
 * 任务 7：后端接口地址配置。
 * <p>
 * 10.0.2.2 是 Android 模拟器访问"宿主机 localhost"的固定映射地址，
 * 直接用 localhost 会指向模拟器自身，导致连接被拒绝。
 * 真机调试时改为电脑在局域网中的 IP，例如 http://192.168.1.10:8080。
 */
public final class ApiConfig {

    public static final String BASE_URL = "http://10.0.2.2:8080";

    /** 员工分页列表大小。 */
    public static final int PAGE_SIZE = 5;

    private ApiConfig() {
    }
}
