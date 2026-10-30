# 实验一：AI 赋能 Android 原生开发综合实验

《移动应用开发（AI 赋能版）》课程实验一（24 学时，个人独立完成）完整代码仓库。

## 一、仓库结构

```
安卓/
├── HelloAndroid/                 # Android 原生客户端（任务 1~9 全部演示入口）
│   ├── app/src/main/java/com/example/helloandroid/
│   │   ├── MainActivity.java          # 任务1 Log 五级日志 + 任务导航
│   │   ├── task2/                     # 任务2 生命周期、Intent 传参与回传、启动模式
│   │   ├── task3/                     # 任务3 四种布局/控件、RecyclerView、聊天室
│   │   ├── broadcast/                 # 任务4 动态/静态广播、有序广播
│   │   ├── storage/ db/               # 任务5 文件存储、SharedPreferences、SQLite
│   │   ├── permission/                # 任务6 运行时权限、自定义 ContentProvider
│   │   ├── network/                   # 任务7 HttpURLConnection + org.json/Gson
│   │   ├── service/                   # 任务8 Service 生命周期、定位与多媒体
│   │   └── emp/                       # 任务9 与 Spring 后端联调的员工 CRUD
│   └── app/src/main/res/layout/       # 17 个布局文件
├── AndroidLabServer/             # 任务7/9 后端：Spring Boot + SpringMVC + MyBatis + MySQL
│   ├── src/main/java/com/example/lab/
│   └── sql/init.sql                   # 建库建表 + 初始数据
├── 实验一_实验报告.docx
└── 实验一_实验步骤指导.docx
```

## 二、环境要求

| 组件 | 版本（本机实测） |
|---|---|
| JDK | 21.0.8（`D:\java\jdk.21`，编译目标 Java 17） |
| Android SDK | Platform 34 / Build-Tools 34.0.0（`D:\Android\Sdk`） |
| Gradle | 8.7（走 `gradlew` 自动下载） |
| Android Gradle Plugin | 8.4.2 |
| Spring Boot | 3.2.5 |
| MyBatis | 3.0.3（mybatis-spring-boot-starter） |
| MySQL | 8.0.46，端口 3306 |
| Maven | 3.9.9 |

## 三、运行步骤

### 1. 初始化数据库

```bat
mysql -u root -p --default-character-set=utf8mb4 < AndroidLabServer\sql\init.sql
```

执行后得到 `android_lab` 库：`t_user`（4 条）、`emp`（7 条）。

### 2. 启动后端

```bat
cd AndroidLabServer
mvn -DskipTests package
java -jar target\android-lab-server-1.0.0.jar
```

启动后监听 `http://localhost:8080`，接口清单：

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/users` | 任务7 用户数组 |
| POST | `/api/users` | 任务7 新增用户 |
| GET | `/api/emps?page=1&size=5` | 任务9 员工分页列表 |
| GET | `/api/emp/{id}` | 任务9 单个员工 |
| POST | `/api/emp` | 任务9 新增员工 |
| PUT | `/api/emp` | 任务9 修改员工 |
| DELETE | `/api/emp/{id}` | 任务9 删除员工 |

### 3. 编译并运行 App

```bat
cd HelloAndroid
gradlew.bat assembleDebug
```

产物：`app/build/outputs/apk/debug/app-debug.apk`

用 Android Studio 打开 `HelloAndroid`，或在模拟器已启动时：

```bat
adb install -r app\build\outputs\apk\debug\app-debug.apk
adb shell am start -n com.example.helloandroid/.MainActivity
```

> 首次在新机器打开需在 `HelloAndroid/local.properties` 中配置
> `sdk.dir=<你的 Android SDK 路径>`（该文件已加入 .gitignore，不入库）。

## 四、关键说明

1. **模拟器访问宿主机后端用 `10.0.2.2`**，不是 `localhost`；真机改为电脑局域网 IP，见
   `network/ApiConfig.java`。
2. **明文 HTTP**：Android 9.0+ 默认禁止，`AndroidManifest.xml` 中已声明
   `android:usesCleartextTraffic="true"`，仅供实验联调，生产应改用 HTTPS。
3. **含中文路径**：工程位于中文目录，`gradle.properties` 中已加
   `android.overridePathCheck=true`，并在 `compileOptions` 指定 UTF-8 编码。
4. **被测库隔离**：教学用的 `android_lab` 与先修课 `ssm_emp` 结构一致但相互独立，
   避免实验中的增删改破坏原有数据。

## 五、提交规范

每个任务至少一次有效提交，提交说明采用 `feat(任务N): 说明` 格式，便于对照实验报告的
"工程与 AI"评分项。
