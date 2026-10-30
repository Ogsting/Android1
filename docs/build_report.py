# -*- coding: utf-8 -*-
"""生成《实验一 实验报告》。

正文引用统一用「」，避免与 Python 字符串定界符冲突。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.shared import Cm, Pt
from docx_kit import (HEI, bullet, code_block, h1, h2, h3, kv_line, new_document,
                      note, numbered, page_break, para, placeholder,
                      reset_numbering, style_run, table, title)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "实验一_实验报告.docx")

doc = new_document("实验一 实验报告")


def qa(question, answer):
    """思考题：加粗问句 + 缩进作答。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1)
    style_run(p.add_run("【问】" + question), size=11, bold=True, font=HEI,
              color=(0x1F, 0x2D, 0x3D))
    p2 = doc.add_paragraph()
    p2.paragraph_format.left_indent = Cm(0.5)
    p2.paragraph_format.space_after = Pt(4)
    style_run(p2.add_run("【答】" + answer), size=11)


title(doc, "《移动应用开发（AI 赋能版）》", "实验一　AI 赋能 Android 原生开发综合实验　实验报告")
para(doc, "课程代码：1960079　|　24 学时　|　设计性、综合性　|　个人独立完成",
     size=10, indent=False, align="center")

# ---------------------------------------------------------------- 基础信息
h2(doc, "基础信息")
kv_line(doc, "实验项目：", "AI 赋能 Android 原生开发综合实验")
kv_line(doc, "实验时间：")
kv_line(doc, "实验地点：")
kv_line(doc, "姓　　名：")
kv_line(doc, "班　　级：")
kv_line(doc, "学　　号：")
kv_line(doc, "指导教师：")

note(doc, "说明：本报告按实验指导书附录二的模板组织，正文按任务 1 到 9 分节。"
          "文中标注为「截图 N 占位」的灰框是运行截图位置，把对应截图粘贴进去后删除占位框即可，"
          "截图清单见文末附录。")

page_break(doc)

# ================================================================ 一
h1(doc, "一、实验目的与任务")

h2(doc, "1.1 实验目的")
para(doc, "本次实验以 Android 原生开发为主线，把课程理论章节的九个知识模块串成一个可运行的综合案例，"
          "目标是把「看得懂」变成「写得出、跑得通、讲得清」。具体目的如下：")
for t in [
    "完成 Android 开发环境搭建、模拟器配置，掌握项目目录结构与 Log 分级日志调试；",
    "掌握 Activity 七大生命周期、Intent 页面跳转与参数传递回传、四种启动模式；",
    "掌握四种基础布局、常用控件与事件处理，能独立完成列表与简易聊天室界面；",
    "理解广播机制，掌握系统广播监听与自定义广播的收发、有序广播的优先级控制；",
    "掌握文件存储、SharedPreferences、SQLite 三种持久化方案，完成通讯录数据库案例；",
    "理解内容提供器与运行时权限机制，实现系统数据读取与自定义 Provider 数据共享；",
    "掌握 HTTP 网络请求与 JSON 解析，完成与 Spring 后端的接口联调；",
    "理解 Service 生命周期，能开发定位与多媒体功能；",
    "完成 Android 客户端与 SpringMVC 后端的综合整合，具备前后端全链路联调能力；",
    "全程规范使用 AI 辅助工具，具备甄别、修正 AI 生成代码的能力。",
]:
    bullet(doc, t, size=11.5)

h2(doc, "1.2 实验任务与学时分配")
table(doc,
      ["任务", "内容", "学时"],
      [
          ["任务 1", "Android 开发环境搭建与项目基础（Log 调试）", "2"],
          ["任务 2", "Activity 生命周期与 Intent 页面通信", "3"],
          ["任务 3", "UI 布局与常用控件（含简易聊天室界面）", "3"],
          ["任务 4", "广播机制（系统广播与自定义广播）", "2"],
          ["任务 5", "数据持久化（文件 / SharedPreferences / SQLite 通讯录）", "4"],
          ["任务 6", "内容提供器与运行时权限", "2"],
          ["任务 7", "网络技术应用（JSON 解析与 Spring 接口联调）", "4"],
          ["任务 8", "后台服务与定位多媒体", "2"],
          ["任务 9", "Android 与 SpringMVC 整合综合案例", "2"],
          ["合计", "—", "24"],
      ],
      widths=[2.2, 11.4, 2.4], first_col_bold=True)

h2(doc, "1.3 实验环境")
table(doc,
      ["类别", "名称与版本（本机实测）", "用途"],
      [
          ["JDK", "Oracle JDK 21.0.8（编译目标 Java 17）", "Java 编译与运行"],
          ["开发工具", "Android Studio（AGP 8.4.2 + Gradle 8.7）", "原生开发"],
          ["SDK", "Android SDK Platform 34、Build-Tools 34.0.0", "编译目标 API"],
          ["运行环境", "Android 模拟器 Pixel_API_34（x86_64）", "应用调试"],
          ["后端", "Spring Boot 3.2.5（内嵌 Tomcat）+ MyBatis 3.0.3 + Maven 3.9.9", "接口服务"],
          ["数据库", "MySQL 8.0.46（utf8mb4，端口 3306）", "数据持久化"],
          ["测试与协作", "Git 2.x、curl / Postman", "版本管理与接口测试"],
          ["AI 辅助工具", "AI 编程助手（对话式代码生成与审查）", "代码生成、纠错、注释"],
      ],
      widths=[2.6, 8.6, 4.8], font_size=9.5)

page_break(doc)

# ================================================================ 二
h1(doc, "二、实验过程描述及重点代码功能注释")

para(doc, "全部任务实现在同一个工程 HelloAndroid 中：MainActivity 作为任务导航入口，"
          "每个任务对应独立的 Activity / Service / Receiver，后端单独放在 AndroidLabServer。"
          "下面按任务顺序记录操作过程、关键代码与运行结果。")

# ---------------------------------------------------------------- 任务 1
h2(doc, "2.1　任务 1　开发环境搭建与项目基础（2 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "安装并配置 JDK 21 与 Android Studio，在命令行用 java -version 验证；"
              "用 sdkmanager --list 确认 Platform 34 与 Build-Tools 34.0.0 已安装。")
numbered(doc, "在 Android Studio 的 SDK Manager 下载 API 34 系统镜像，创建 Pixel 系列 AVD 并启动验证。")
numbered(doc, "新建 Empty Views Activity 工程 HelloAndroid，观察目录结构："
              "app/src/main/java 放源码，res/layout 放布局，res/values 放字符串与主题，"
              "AndroidManifest.xml 是清单文件。")
numbered(doc, "在 MainActivity.onCreate 中输出五级日志，在 Logcat 用 tag:HelloAndroid 过滤查看。")
numbered(doc, "运行 gradlew.bat assembleDebug 从命令行编译，确认脱离 IDE 也能出包。")

note(doc, "工程位于含中文的目录 D:\\HOMEWORK\\HomeWork\\安卓，AGP 会直接拒绝构建。"
          "处理方式见第三章问题 1。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           'private static final String TAG = "HelloAndroid";\n'
           '\n'
           '@Override\n'
           'protected void onCreate(Bundle savedInstanceState) {\n'
           '    super.onCreate(savedInstanceState);\n'
           '    setContentView(R.layout.activity_main);\n'
           '\n'
           '    // 五级日志验证：级别由低到高 v < d < i < w < e\n'
           '    Log.v(TAG, "onCreate: verbose 日志，最细粒度，仅本地调试使用");\n'
           '    Log.d(TAG, "onCreate: debug 日志，开发期调试信息");\n'
           '    Log.i(TAG, "onCreate: info 日志，关键流程节点");\n'
           '    Log.w(TAG, "onCreate: warn 日志，潜在风险提示");\n'
           '    Log.e(TAG, "onCreate: error 日志，错误但未导致崩溃");\n'
           '\n'
           '    bindNavigation();\n'
           '}',
           caption="代码 2-1　MainActivity 五级日志输出（MainActivity.java）")
para(doc, "TAG 用类名常量，便于在 Logcat 里按 tag 精确过滤；"
          "实际项目中级别选择应按「上线后还需不需要看」来定：v 与 d 属于开发期信息，"
          "发布版本应关闭，仅保留 i 以上的关键节点与错误。")

h3(doc, "（3）运行结果")
placeholder(doc, 1, "任务 1　Logcat 五级日志输出",
            "Logcat 过滤 tag:HelloAndroid，能同时看到 V/D/I/W/E 五条日志及时间戳", 4.6)
placeholder(doc, 2, "任务 1　Project 目录结构",
            "Android Studio 左侧 Project 视图展开 java / res / layout / values / Manifest", 4.6)

# ---------------------------------------------------------------- 任务 2
h2(doc, "2.2　任务 2　Activity 生命周期与 Intent 页面通信（3 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "新建 FirstActivity 与 SecondActivity，在两个 Activity 中重写全部生命周期方法并打印日志。")
numbered(doc, "分别通过正常跳转、按 Home 键、旋转屏幕、finish() 四种操作，"
              "在 Logcat 观察 onCreate → onStart → onResume → onPause → onStop → onDestroy 的切换过程。")
numbered(doc, "用显式 Intent 跳转，通过 Bundle 传递 String、int、boolean 三种类型数据。")
numbered(doc, "用 registerForActivityResult 接收 SecondActivity 回传的结果。")
numbered(doc, "在 AndroidManifest.xml 中依次把 SecondActivity 的 launchMode 改成四种模式，"
              "反复跳转并观察任务栈中实例数量变化。")
numbered(doc, "另外编写一个隐式 Intent 打开系统浏览器，对比显式 Intent 的差别。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           '// 新版结果回调 API：替代已废弃的 startActivityForResult / onActivityResult\n'
           '// 必须在 onCreate 之前（字段初始化阶段）注册\n'
           'private final ActivityResultLauncher<Intent> secondLauncher =\n'
           '        registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {\n'
           '            if (result.getResultCode() == RESULT_OK && result.getData() != null) {\n'
           '                String reply = result.getData().getStringExtra("result");\n'
           '                tvResult.setText("收到回传：" + reply);\n'
           '            }\n'
           '        });\n'
           '\n'
           'Button btnJump = findViewById(R.id.btn_jump);\n'
           'btnJump.setOnClickListener(v -> {\n'
           '    Intent intent = new Intent(FirstActivity.this, SecondActivity.class);\n'
           '    intent.putExtra("username", "张三");\n'
           '    intent.putExtra("age", 20);\n'
           '    intent.putExtra("isVip", true);\n'
           '    secondLauncher.launch(intent);   // 用 launcher 启动才能拿到回传结果\n'
           '});',
           caption="代码 2-2　FirstActivity 显式跳转、传参与结果回传")

code_block(doc,
           '// 接收上一个页面传来的参数\n'
           'Intent intent = getIntent();\n'
           'String username = intent.getStringExtra("username");\n'
           'int age = intent.getIntExtra("age", -1);\n'
           'boolean isVip = intent.getBooleanExtra("isVip", false);\n'
           '\n'
           '// 回传结果并结束当前页面\n'
           'Button btnBack = findViewById(R.id.btn_reply);\n'
           'btnBack.setOnClickListener(v -> {\n'
           '    Intent reply = new Intent();\n'
           '    reply.putExtra("result", "欢迎 " + username);\n'
           '    setResult(RESULT_OK, reply);   // 先 setResult\n'
           '    finish();                      // 再 finish，否则回传数据会丢失\n'
           '});',
           caption="代码 2-3　SecondActivity 接收参数并回传结果")

para(doc, "四种启动模式实测结论：standard 每次跳转都新建实例，任务栈里会堆叠多个 SecondActivity；"
          "singleTop 在栈顶已有同类型实例时复用，不新建；"
          "singleTask 在整个任务栈中只保留一个实例，再次启动会清掉它上面的 Activity；"
          "singleInstance 独占一个新任务栈，其他 Activity 不会进入该栈。")

h3(doc, "（3）运行结果")
placeholder(doc, 3, "任务 2　SecondActivity 接收到的参数",
            "显示 username = 张三、age = 20、isVip = true", 4.2)
placeholder(doc, 4, "任务 2　结果回传后的 FirstActivity",
            "界面显示「收到回传：欢迎 张三」", 4.2)
placeholder(doc, 5, "任务 2　生命周期日志序列",
            "Logcat 中完整的一次 onPause → onStop → onRestart 序列，或四种启动模式对比", 4.6)

page_break(doc)

# ---------------------------------------------------------------- 任务 3
h2(doc, "2.3　任务 3　UI 布局与常用控件（3 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "在登录页里同时使用四种布局：根布局 LinearLayout、标题区 FrameLayout、"
              "按钮区 RelativeLayout、表单区 ConstraintLayout。")
numbered(doc, "练习 TextView、EditText、Button、ImageView、RadioButton、CheckBox、Switch "
              "七种以上控件的属性、赋值、取值与点击事件。")
numbered(doc, "用 layout_weight 做三块区域的权重分配，理解 0dp + weight 的用法。")
numbered(doc, "编写 RecyclerView 联系人列表：item 布局、Adapter、ViewHolder，绑定模拟数据并处理点击。")
numbered(doc, "综合以上完成简易聊天室：顶部标题栏 + 中部消息列表（左右气泡）+ 底部输入框与发送按钮。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           '<!-- 根布局 LinearLayout（垂直）+ layout_weight 分配剩余空间 -->\n'
           '<LinearLayout android:orientation="vertical" ...>\n'
           '\n'
           '    <!-- FrameLayout：标题与副标题叠加 -->\n'
           '    <FrameLayout ...>\n'
           '        <TextView android:background="#3F51B5" android:gravity="center" ... />\n'
           '        <ImageView android:layout_gravity="end|top" ... />\n'
           '    </FrameLayout>\n'
           '\n'
           '    <!-- ConstraintLayout：表单区扁平化，避免多层嵌套 -->\n'
           '    <androidx.constraintlayout.widget.ConstraintLayout ...>\n'
           '        <EditText android:id="@+id/et_username"\n'
           '                  app:layout_constraintStart_toEndOf="@id/tv_user_label" ... />\n'
           '    </androidx.constraintlayout.widget.ConstraintLayout>\n'
           '\n'
           '    <!-- layout_weight 演示：0dp + weight 才能正确等分剩余空间 -->\n'
           '    <LinearLayout android:layout_height="0dp" android:layout_weight="1" ...>\n'
           '        <TextView android:layout_width="0dp" android:layout_weight="1" ... />\n'
           '        <TextView android:layout_width="0dp" android:layout_weight="2" ... />\n'
           '    </LinearLayout>\n'
           '</LinearLayout>',
           caption="代码 2-4　登录页四种布局组合（activity_login.xml 节选）")

code_block(doc,
           '/** ViewHolder：持有子项内部控件引用，避免重复 findViewById。 */\n'
           'public static class VH extends RecyclerView.ViewHolder {\n'
           '    final TextView tvName;\n'
           '    final TextView tvPhone;\n'
           '\n'
           '    public VH(@NonNull View itemView) {\n'
           '        super(itemView);\n'
           '        tvName = itemView.findViewById(R.id.tv_name);\n'
           '        tvPhone = itemView.findViewById(R.id.tv_phone);\n'
           '    }\n'
           '}\n'
           '\n'
           '@NonNull\n'
           '@Override\n'
           'public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {\n'
           '    // inflate 第三个参数必须为 false，否则子项会丢失父布局的 LayoutParams\n'
           '    View v = LayoutInflater.from(parent.getContext())\n'
           '            .inflate(R.layout.item_contact, parent, false);\n'
           '    return new VH(v);\n'
           '}\n'
           '\n'
           '@Override\n'
           'public void onBindViewHolder(@NonNull VH holder, int position) {\n'
           '    Contact c = data.get(position);\n'
           '    holder.tvName.setText(c.getName());\n'
           '    holder.tvPhone.setText(c.getPhone());\n'
           '    holder.itemView.setOnClickListener(v -> listener.onItemClick(c));\n'
           '}',
           caption="代码 2-5　RecyclerView 适配器与 ViewHolder（ContactAdapter.java）")

para(doc, "聊天室通过判断消息的 fromMe 标志，动态设置这一行的 gravity 与气泡背景色，"
          "实现左右气泡区分：我方靠右、深蓝底白字；对方靠左、浅灰底深色字。")

h3(doc, "（3）运行结果")
placeholder(doc, 6, "任务 3　登录页（四种布局与常用控件）",
            "完整登录页，能看出标题区、表单区、单选/复选/开关与权重区域", 4.8)
placeholder(doc, 7, "任务 3　RecyclerView 联系人列表",
            "至少 6 条联系人，含姓名与电话", 4.4)
placeholder(doc, 8, "任务 3　简易聊天室界面",
            "左右两种气泡，至少各一条消息", 4.6)

page_break(doc)

# ---------------------------------------------------------------- 任务 4
h2(doc, "2.4　任务 4　广播机制（2 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "动态注册广播接收器监听网络变化广播，在 onDestroy 中注销。")
numbered(doc, "创建 MyBroadcastReceiver，在 AndroidManifest.xml 中静态注册并配置 action，用 sendBroadcast 发送。")
numbered(doc, "对比静态注册与动态注册的差异：前者常驻、后者随组件生命周期。")
numbered(doc, "使用 sendOrderedBroadcast 并为两个接收器设置 priority 100 / 50，观察投递顺序与结果传递。")
numbered(doc, "针对 Android 8.0 以后静态注册接收隐式广播受限的问题，发送时用 setPackage 限定包名。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           '// 1) 动态注册：代码中注册，生命周期随 Activity\n'
           'IntentFilter filter = new IntentFilter();\n'
           'filter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);\n'
           'networkReceiver = new NetworkChangeReceiver();\n'
           'registerReceiver(networkReceiver, filter);\n'
           'registered = true;\n'
           '\n'
           '// 2) 发送普通自定义广播（静态接收器可收到）\n'
           'Intent intent = new Intent(MyBroadcastReceiver.ACTION_CUSTOM);\n'
           'intent.setPackage(getPackageName());  // 限定本应用，规避 Android 8.0+ 隐式广播限制\n'
           'intent.putExtra("msg", "你好，静态接收器");\n'
           'sendBroadcast(intent);\n'
           '\n'
           '// 3) 发送有序广播：priority 大的先收到\n'
           'Intent ordered = new Intent("com.example.helloandroid.ORDERED_BROADCAST");\n'
           'ordered.setPackage(getPackageName());\n'
           'ordered.putExtra("msg", "有序广播内容");\n'
           'sendOrderedBroadcast(ordered, null);\n'
           '\n'
           '@Override\n'
           'protected void onDestroy() {\n'
           '    super.onDestroy();\n'
           '    // 动态注册的接收器必须注销，否则报 leaked IntentReceiver 异常\n'
           '    if (registered) {\n'
           '        unregisterReceiver(networkReceiver);\n'
           '        registered = false;\n'
           '    }\n'
           '}',
           caption="代码 2-6　广播的动态注册、发送与注销（BroadcastActivity.java）")

h3(doc, "（3）运行结果")
placeholder(doc, 9, "任务 4　网络变化广播",
            "开关飞行模式后界面显示「网络状态变化：已断开」或已连接", 4.2)
placeholder(doc, 10, "任务 4　有序广播投递顺序",
            "Logcat 中 OrderedReceiverA（priority 100）先于 OrderedReceiverB（priority 50）", 4.6)

# ---------------------------------------------------------------- 任务 5
h2(doc, "2.5　任务 5　数据持久化（4 学时，本任务为重点）")

h3(doc, "（1）操作过程")
para(doc, "任务 5-1 文件存储与 SharedPreferences：")
reset_numbering()
numbered(doc, "用 openFileOutput 把文本写入内部存储，再用 openFileInput 读回，理解 MODE_PRIVATE 的含义。")
numbered(doc, "用 SharedPreferences 实现记住密码功能，理解 commit 与 apply 的区别。")
para(doc, "任务 5-2 SQLite 通讯录：")
reset_numbering()
numbered(doc, "编写实体类 Contact（id、name、phone、email、gender）。")
numbered(doc, "继承 SQLiteOpenHelper 创建 contact.db 与 contact 表，"
              "并把 VERSION 从 1 提升到 2，在 onUpgrade 中用 ALTER TABLE 增加 gender 列。")
numbered(doc, "编写 ContactDao，用参数化 SQL 完成增、删、改、查，并演示批量插入事务。")
numbered(doc, "用 RecyclerView 展示通讯录，支持新增、编辑（点击）、删除（长按）、按姓名模糊查询。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           'public static final String DB_NAME = "contact.db";\n'
           '/** 版本号从 1 升到 2，用于演示 onUpgrade 增加 gender 列。 */\n'
           'public static final int VERSION = 2;\n'
           '\n'
           '@Override\n'
           'public void onCreate(SQLiteDatabase db) {\n'
           '    // onCreate 只在数据库文件第一次创建时执行一次\n'
           '    db.execSQL("CREATE TABLE contact(" +\n'
           '            "id INTEGER PRIMARY KEY AUTOINCREMENT," +\n'
           '            "name TEXT NOT NULL," +\n'
           '            "phone TEXT," +\n'
           '            "email TEXT)");\n'
           '}\n'
           '\n'
           '@Override\n'
           'public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {\n'
           '    if (oldVersion < 2) {\n'
           '        // 增量升级：只加列，不丢已有数据\n'
           '        db.execSQL("ALTER TABLE contact ADD COLUMN gender TEXT");\n'
           '    }\n'
           '}',
           caption="代码 2-7　数据库创建与版本升级（ContactDbHelper.java）")

code_block(doc,
           '/** 查询：按姓名模糊查询，关键字为空则返回全部，按 id 倒序。 */\n'
           'public List<Contact> query(String keyword) {\n'
           '    SQLiteDatabase db = helper.getReadableDatabase();\n'
           '    List<Contact> list = new ArrayList<>();\n'
           '\n'
           '    String selection = null;\n'
           '    String[] args = null;\n'
           '    if (keyword != null && !keyword.trim().isEmpty()) {\n'
           '        selection = "name LIKE ?";              // 参数化，杜绝 SQL 注入\n'
           '        args = new String[]{"%" + keyword.trim() + "%"};\n'
           '    }\n'
           '\n'
           '    // try-with-resources 保证 Cursor 一定被关闭，避免泄漏\n'
           '    try (Cursor cursor = db.query("contact", null, selection, args,\n'
           '            null, null, "id DESC")) {\n'
           '        while (cursor.moveToNext()) {\n'
           '            Contact c = new Contact();\n'
           '            c.setId(cursor.getLong(cursor.getColumnIndexOrThrow("id")));\n'
           '            c.setName(cursor.getString(cursor.getColumnIndexOrThrow("name")));\n'
           '            list.add(c);\n'
           '        }\n'
           '    }\n'
           '    return list;\n'
           '}\n'
           '\n'
           '/** 批量导入：要么全部成功，要么全部回滚。 */\n'
           'public void insertBatch(List<Contact> contacts) {\n'
           '    SQLiteDatabase db = helper.getWritableDatabase();\n'
           '    db.beginTransaction();\n'
           '    try {\n'
           '        for (Contact c : contacts) {\n'
           '            ContentValues cv = new ContentValues();\n'
           '            cv.put("name", c.getName());\n'
           '            cv.put("phone", c.getPhone());\n'
           '            db.insert("contact", null, cv);\n'
           '        }\n'
           '        db.setTransactionSuccessful();   // 不调用则 endTransaction 时全部回滚\n'
           '    } finally {\n'
           '        db.endTransaction();\n'
           '    }\n'
           '}',
           caption="代码 2-8　参数化查询与事务（ContactDao.java）")

h3(doc, "（3）运行结果")
placeholder(doc, 11, "任务 5　文件存储与 SharedPreferences",
            "写入后读回的文件内容，以及 SharedPreferences 的 username / remember 值", 4.4)
placeholder(doc, 12, "任务 5　SQLite 通讯录列表",
            "至少 3 条联系人，能看到姓名、电话、邮箱", 4.4)
placeholder(doc, 13, "任务 5　事务批量插入结果",
            "点击「事务批量插入 3 条」后列表条数增加", 4.2)

page_break(doc)

# ---------------------------------------------------------------- 任务 6
h2(doc, "2.6　任务 6　内容提供器与运行时权限（2 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "动态申请 READ_CONTACTS 危险权限，在 onRequestPermissionsResult 中处理授权结果。")
numbered(doc, "通过 ContentResolver 读取系统通讯录并展示前 10 条，理解 URI 与系统 ContentProvider 的作用。")
numbered(doc, "创建自定义 ContentProvider，对外共享任务 5 的通讯录数据："
              "实现 insert / query / update / delete / getType，用 UriMatcher 匹配 URI。")
numbered(doc, "在 AndroidManifest.xml 中注册 provider 并设置 exported 属性。")
numbered(doc, "在 App 内部用 ContentResolver 访问自定义 Provider，验证注册与 URI 匹配是否生效。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           '/** 先检查再申请，这是 Android 6.0 之后的固定套路。 */\n'
           'private void checkAndRead() {\n'
           '    if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)\n'
           '            != PackageManager.PERMISSION_GRANTED) {\n'
           '        // 未授权：发起申请，结果回到 onRequestPermissionsResult\n'
           '        ActivityCompat.requestPermissions(this,\n'
           '                new String[]{Manifest.permission.READ_CONTACTS}, REQ_READ_CONTACTS);\n'
           '    } else {\n'
           '        readContacts();\n'
           '    }\n'
           '}\n'
           '\n'
           '@Override\n'
           'public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,\n'
           '                                       @NonNull int[] grantResults) {\n'
           '    super.onRequestPermissionsResult(requestCode, permissions, grantResults);\n'
           '    if (requestCode == REQ_READ_CONTACTS) {\n'
           '        // grantResults 可能为空（用户直接取消），必须判空\n'
           '        if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {\n'
           '            readContacts();\n'
           '        } else {\n'
           '            Toast.makeText(this, "权限被拒绝，无法读取通讯录", Toast.LENGTH_SHORT).show();\n'
           '        }\n'
           '    }\n'
           '}',
           caption="代码 2-9　运行时权限申请（PermissionContactActivity.java）")

code_block(doc,
           'public static final String AUTHORITY = "com.example.helloandroid.provider";\n'
           'public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/contact");\n'
           '\n'
           'private static final int CODE_CONTACT_DIR = 0;\n'
           'private static final int CODE_CONTACT_ITEM = 1;\n'
           'private static final UriMatcher MATCHER = new UriMatcher(UriMatcher.NO_MATCH);\n'
           '\n'
           'static {\n'
           '    MATCHER.addURI(AUTHORITY, "contact", CODE_CONTACT_DIR);    // 整个表\n'
           '    MATCHER.addURI(AUTHORITY, "contact/#", CODE_CONTACT_ITEM); // 单条记录\n'
           '}\n'
           '\n'
           '@Nullable\n'
           '@Override\n'
           'public Cursor query(@NonNull Uri uri, String[] projection, String selection,\n'
           '                    String[] selectionArgs, String sortOrder) {\n'
           '    SQLiteDatabase db = helper.getReadableDatabase();\n'
           '    Cursor cursor;\n'
           '    switch (MATCHER.match(uri)) {\n'
           '        case CODE_CONTACT_DIR:\n'
           '            cursor = db.query("contact", projection, selection, selectionArgs,\n'
           '                    null, null, sortOrder);\n'
           '            break;\n'
           '        case CODE_CONTACT_ITEM:\n'
           '            String id = uri.getPathSegments().get(1);\n'
           '            cursor = db.query("contact", projection, "id = ?", new String[]{id},\n'
           '                    null, null, sortOrder);\n'
           '            break;\n'
           '        default:\n'
           '            throw new IllegalArgumentException("未知 URI: " + uri);\n'
           '    }\n'
           '    cursor.setNotificationUri(getContext().getContentResolver(), uri);\n'
           '    return cursor;\n'
           '}',
           caption="代码 2-10　自定义 ContentProvider 的 URI 匹配与查询（ContactProvider.java）")

h3(doc, "（3）运行结果")
placeholder(doc, 14, "任务 6　运行时权限申请弹窗",
            "READ_CONTACTS 权限授权对话框", 4.2)
placeholder(doc, 15, "任务 6　自定义 ContentProvider 查询结果",
            "通过 ContentResolver 读到任务 5 添加的联系人", 4.4)

# ---------------------------------------------------------------- 任务 7
h2(doc, "2.7　任务 7　网络技术应用（4 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "搭建本地 Spring 后端，提供返回 JSON 数组的 /api/users 接口。")
numbered(doc, "用 HttpURLConnection 发起 GET 与 POST 请求，注意在子线程执行并捕获异常。")
numbered(doc, "分别用 org.json 的 JSONArray / JSONObject 与 Gson 解析同一份数据，对比两种方式。")
numbered(doc, "封装通用网络请求工具类 HttpUtil：GET / POST / PUT / DELETE、回调、主线程切换、异常统一处理。")
numbered(doc, "处理 Android 9.0 以上默认禁止明文 HTTP 的限制，并在模拟器上用 10.0.2.2 访问宿主机。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           'private static void request(final String method, final String url,\n'
           '                            final String jsonBody, final Callback callback) {\n'
           '    // Android 禁止主线程网络操作，必须另起线程\n'
           '    new Thread(() -> {\n'
           '        HttpURLConnection conn = null;\n'
           '        try {\n'
           '            conn = (HttpURLConnection) new URL(url).openConnection();\n'
           '            conn.setRequestMethod(method);\n'
           '            conn.setConnectTimeout(5000);\n'
           '            conn.setReadTimeout(5000);\n'
           '            // 声明请求体为 JSON，否则后端可能返回 415\n'
           '            conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");\n'
           '\n'
           '            if (jsonBody != null) {\n'
           '                conn.setDoOutput(true);\n'
           '                try (OutputStream os = conn.getOutputStream()) {\n'
           '                    os.write(jsonBody.getBytes(StandardCharsets.UTF_8));\n'
           '                }\n'
           '            }\n'
           '\n'
           '            int code = conn.getResponseCode();\n'
           '            if (code >= 200 && code < 300) {\n'
           '                final String result = readAll(conn.getInputStream());\n'
           '                MAIN.post(() -> callback.onSuccess(result));  // 切回主线程再更新 UI\n'
           '            } else {\n'
           '                final String err = "HTTP " + code + "：" + readAll(conn.getErrorStream());\n'
           '                MAIN.post(() -> callback.onError(err));\n'
           '            }\n'
           '        } catch (Exception e) {\n'
           '            final String msg = e.getClass().getSimpleName() + "：" + e.getMessage();\n'
           '            MAIN.post(() -> callback.onError(msg));\n'
           '        } finally {\n'
           '            if (conn != null) conn.disconnect();\n'
           '        }\n'
           '    }).start();\n'
           '}',
           caption="代码 2-11　网络请求工具类核心（HttpUtil.java）")

code_block(doc,
           '// 用 Gson 的 TypeToken 反序列化为 List<User>\n'
           'Type type = new TypeToken<List<User>>() {}.getType();\n'
           'List<User> users = new Gson().fromJson(json, type);\n'
           '\n'
           '// 对比：org.json 逐字段手工取值\n'
           'JSONArray array = new JSONArray(json);\n'
           'for (int i = 0; i < array.length(); i++) {\n'
           '    JSONObject o = array.getJSONObject(i);\n'
           '    long id = o.getLong("id");\n'
           '    String nickname = o.optString("nickname");\n'
           '}',
           caption="代码 2-12　Gson 与 org.json 两种解析方式对比（NetworkActivity.java）")

h3(doc, "（3）运行结果")
placeholder(doc, 16, "任务 7　org.json 与 Gson 解析结果",
            "两种方式都列出 4 个用户，底部显示「共 4 条」", 4.6)
placeholder(doc, 17, "任务 7　POST 新增用户与异常兜底",
            "POST 成功的返回内容，或后端未启动时的错误提示", 4.6)

page_break(doc)

# ---------------------------------------------------------------- 任务 8
h2(doc, "2.8　任务 8　后台服务与定位多媒体（2 学时）")

h3(doc, "（1）操作过程")
numbered(doc, "创建 MyService，演示 startService / stopService 与 onCreate、onStartCommand、onDestroy 生命周期。")
numbered(doc, "通过 bindService / unbindService 实现绑定式通信，用 LocalBinder 暴露服务方法，对比两种方式差异。")
numbered(doc, "使用系统 LocationManager 获取一次定位，理解 ACCESS_FINE_LOCATION 与 "
              "ACCESS_COARSE_LOCATION 的运行时时申请。")
numbered(doc, "使用 MediaPlayer 播放网络音频，掌握异步准备与资源释放；用 Intent 调用系统相机拍照。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           'public class MyService extends Service {\n'
           '\n'
           '    /** 供绑定方直接调用的 Binder 实现。 */\n'
           '    public class LocalBinder extends Binder {\n'
           '        public MyService getService() {\n'
           '            return MyService.this;\n'
           '        }\n'
           '    }\n'
           '\n'
           '    private final IBinder binder = new LocalBinder();\n'
           '\n'
           '    @Override\n'
           '    public void onCreate() {\n'
           '        super.onCreate();\n'
           '        Log.d(TAG, "onCreate：服务创建");\n'
           '    }\n'
           '\n'
           '    @Override\n'
           '    public int onStartCommand(Intent intent, int flags, int startId) {\n'
           '        Log.d(TAG, "onStartCommand：startId = " + startId);\n'
           '        // START_STICKY：服务被系统杀死后尝试重建\n'
           '        return START_STICKY;\n'
           '    }\n'
           '\n'
           '    @Override\n'
           '    public IBinder onBind(Intent intent) {\n'
           '        return binder;   // 绑定式入口，调用方拿到 Binder 后可直接调用服务方法\n'
           '    }\n'
           '\n'
           '    /** 绑定式调用的业务方法，用于验证 Activity 与服务确实通信成功。 */\n'
           '    public int increase() {\n'
           '        return ++counter;\n'
           '    }\n'
           '}',
           caption="代码 2-13　Service 双启动方式支持（MyService.java）")

code_block(doc,
           '/** ServiceConnection 回调运行在主线程，拿到 Binder 后即可强转并调用服务方法。 */\n'
           'private final ServiceConnection connection = new ServiceConnection() {\n'
           '    @Override\n'
           '    public void onServiceConnected(ComponentName name, IBinder service) {\n'
           '        MyService.LocalBinder binder = (MyService.LocalBinder) service;\n'
           '        boundService = binder.getService();\n'
           '        isBound = true;\n'
           '        tvStatus.append("\\n绑定成功，调用服务方法 increase() = " + boundService.increase());\n'
           '    }\n'
           '\n'
           '    @Override\n'
           '    public void onServiceDisconnected(ComponentName name) {\n'
           '        isBound = false;\n'
           '        boundService = null;\n'
           '    }\n'
           '};',
           caption="代码 2-14　绑定式服务的连接回调（ServiceActivity.java）")

h3(doc, "（3）运行结果")
placeholder(doc, 18, "任务 8　Service 生命周期日志",
            "Logcat 中 onCreate → onStartCommand → onDestroy 序列（tag:MyService）", 4.6)
placeholder(doc, 19, "任务 8　定位与多媒体",
            "定位得到的经纬度与精度，或 MediaPlayer 播放状态", 4.4)

# ---------------------------------------------------------------- 任务 9
h2(doc, "2.9　任务 9　Android 与 SpringMVC 整合综合案例（2 学时）")

h3(doc, "（1）操作过程")
para(doc, "后端部分：")
reset_numbering()
numbered(doc, "用 Spring Boot + SpringMVC + MyBatis 搭建员工管理接口，"
              "数据库复用先修课 SSM 项目的 emp 表结构（新建 android_lab 库，避免破坏原数据）。")
numbered(doc, "提供 REST 风格接口：GET /api/emps 分页列表、GET /api/emp/{id}、POST /api/emp、"
              "PUT /api/emp、DELETE /api/emp/{id}。")
numbered(doc, "Service 层把页码换算成 offset 并做下限保护，Mapper 用动态 SQL 只更新非空字段。")
numbered(doc, "先用 curl / Postman 单独验证接口，再进行 App 联调。")
para(doc, "客户端部分：")
reset_numbering()
numbered(doc, "把任务 7 的 HttpUtil 与员工列表 / 表单页面整合，启动加载分页员工列表。")
numbered(doc, "表单新增员工（POST JSON，Gson 序列化，Content-Type 为 application/json）。")
numbered(doc, "点击编辑（PUT 请求）、长按删除（DELETE 请求）。")
numbered(doc, "提供加载中提示、空数据提示、网络异常统一提示。")

h3(doc, "（2）重点代码与注释")
code_block(doc,
           '/**\n'
           ' * 员工业务层。分页参数在这里换算成 offset，Controller 只负责接收请求与包装响应。\n'
           ' */\n'
           '@Service\n'
           'public class EmpService {\n'
           '\n'
           '    private final EmpMapper empMapper;\n'
           '\n'
           '    public EmpService(EmpMapper empMapper) {\n'
           '        this.empMapper = empMapper;\n'
           '    }\n'
           '\n'
           '    public Map<String, Object> page(int page, int size) {\n'
           '        // 页码与页大小做下限保护，避免负数导致 SQL 报错\n'
           '        int safePage = Math.max(page, 1);\n'
           '        int safeSize = Math.max(size, 1);\n'
           '        int offset = (safePage - 1) * safeSize;\n'
           '\n'
           '        List<Emp> list = empMapper.findPage(offset, safeSize);\n'
           '        long total = empMapper.count();\n'
           '\n'
           '        Map<String, Object> data = new LinkedHashMap<>();\n'
           '        data.put("total", total);\n'
           '        data.put("page", safePage);\n'
           '        data.put("size", safeSize);\n'
           '        data.put("list", list);\n'
           '        return data;\n'
           '    }\n'
           '}',
           caption="代码 2-15　分页业务逻辑（EmpService.java）")

code_block(doc,
           '<!-- 动态 SQL：只更新前端传了值的字段，未传的字段保持原值 -->\n'
           '<update id="update" parameterType="com.example.lab.entity.Emp">\n'
           '    UPDATE emp\n'
           '    <set>\n'
           '        <if test="empName != null and empName != \'\'">emp_name = #{empName},</if>\n'
           '        <if test="dept != null and dept != \'\'">dept = #{dept},</if>\n'
           '        <if test="post != null and post != \'\'">post = #{post},</if>\n'
           '        <if test="salary != null">salary = #{salary},</if>\n'
           '        <if test="status != null">status = #{status},</if>\n'
           '    </set>\n'
           '    WHERE emp_id = #{empId}\n'
           '</update>',
           caption="代码 2-16　MyBatis 动态 SQL 更新（EmpMapper.xml 节选）")

code_block(doc,
           '@GetMapping("/emps")\n'
           'public Map<String, Object> page(@RequestParam(defaultValue = "1") int page,\n'
           '                                @RequestParam(defaultValue = "5") int size) {\n'
           '    // 直接返回 {total,page,size,list}，与客户端 EmpListActivity 的解析结构一致\n'
           '    return empService.page(page, size);\n'
           '}',
           caption="代码 2-17　分页接口（EmpController.java 节选）")

h3(doc, "（3）联调结果")
para(doc, "用 curl 依次验证了七个接口：GET /api/users 返回 4 条用户；"
          "GET /api/emps?page=1&size=5 返回 total=7、list 长度 5；"
          "POST /api/emp 新增成功（empId=8）；PUT /api/emp 修改岗位与薪资生效；"
          "DELETE /api/emp/8 删除后 total 回到 7；POST /api/users 返回回填 id 的对象。"
          "中文在 MySQL、后端、客户端三处均未出现乱码。")

placeholder(doc, 20, "任务 9　员工列表（分页）",
            "第一页 5 条员工 + 「第 1 页加载完成，共 7 条」统计文字", 4.6)
placeholder(doc, 21, "任务 9　新增与修改员工",
            "新增成功后列表出现新员工，以及修改岗位后的效果", 4.6)
placeholder(doc, 22, "任务 9　数据库一致性核对",
            "MySQL 中 SELECT emp_id, emp_name, dept, post FROM emp 的结果，与 App 显示一致", 4.4)

page_break(doc)

# ================================================================ 三
h1(doc, "三、实验错误描述及改正方式")

para(doc, "以下问题都是在本次实验过程中真实遇到并解决的，按「现象 / 排查思路 / 解决方法 / 整改结果」记录。")

issues = [
    ("问题 1　Gradle 构建直接失败：项目路径含非 ASCII 字符",
     "同步或编译时立刻失败，报 Your project path contains non-ASCII characters. "
     "This will most likely cause the build to fail on Windows，一条编译任务都没有执行。",
     "先看报错指向，确认工程位于 D:\\HOMEWORK\\HomeWork\\安卓，路径里有中文「安卓」。"
     "搜索 AGP 源码可知这是 AGP 对 Windows 路径的主动拦截，不是编码错误；"
     "同时怀疑中文注释在默认 GBK 下还会乱码，属于同一类问题。",
     "在 gradle.properties 中加入 android.overridePathCheck=true 放行路径检查；"
     "并在 app/build.gradle 的 compileOptions 中加 encoding \"UTF-8\"，"
     "杜绝中文注释与字符串乱码。",
     "重新执行 assembleDebug，BUILD SUCCESSFUL，34 个任务全部执行，产出 app-debug.apk（约 5.7 MB）。"
     "后续未再出现路径或编码相关错误。"),

    ("问题 2　后端启动成功但接口 500：Invalid bound statement (not found)",
     "Spring Boot 正常启动，Tomcat 监听 8080，但访问 /api/users 返回 500，"
     "堆栈为 org.apache.ibatis.binding.BindingException: "
     "Invalid bound statement (not found): com.example.lab.mapper.UserMapper.findAll。",
     "先确认接口层没问题：Mapper 接口有 @Mapper，@MapperScan 指向 com.example.lab.mapper，"
     "方法名 findAll 与 XML 的 id 完全一致。再想 MyBatis 的映射来源只有两类：注解或 XML，"
     "而这里 SQL 写在 XML 里。于是怀疑 XML 根本没被加载——检查发现 application.yml 里只配了 "
     "map-underscore-to-camel-case 与 type-aliases-package，没有 mapper-locations，"
     "于是 MyBatis 没有扫描 resources/mapper 目录。",
     "在 application.yml 的 mybatis 节点下显式加入 "
     "mapper-locations: classpath*:/mapper/**/*.xml，重新打包并启动。",
     "接口恢复正常：/api/users 返回 4 条中文正确的 JSON；/api/emps 返回 total=7。"
     "为避免同类问题，我在代码注释里写明了这一项的用途，并把该故障记入报告的常见问题表。"),

    ("问题 3　App 请求后端始终连接被拒绝",
     "客户端点 GET 请求后界面提示 Connection refused，后端在电脑浏览器里访问却是正常的。",
     "先确认后端存活（浏览器能打开 http://localhost:8080/api/users），"
     "说明问题在客户端侧地址。回想模拟器的网络模型：模拟器是一个独立虚拟机，"
     "它自己的 localhost 指向模拟器内部，而不是宿主机，因此必须用专门映射宿主机回环地址的 10.0.2.2。",
     "把 ApiConfig 里的 BASE_URL 从 http://localhost:8080 改为 http://10.0.2.2:8080，"
     "并在类注释里写明真机调试应换成本机局域网 IP。",
     "GET 与 POST 请求全部成功，任务 7 与任务 9 的联调正常。"),

    ("问题 4　明文 HTTP 请求被系统拦截",
     "接口地址确认无误、后端也在运行，但请求仍失败，Logcat 中出现 "
     "CLEARTEXT communication to 10.0.2.2 not permitted by network security policy。",
     "读报错信息可知是 Android 9.0（API 28）起默认禁止明文 HTTP，"
     "而本项目联调的后端是 http 而不是 https。这不是代码写错，是平台安全策略。",
     "在 AndroidManifest.xml 的 application 节点加 android:usesCleartextTraffic=\"true\"，"
     "仅对本次教学联调放开；生产环境应配置 HTTPS 或使用 networkSecurityConfig 限定域名。",
     "明文请求放行，任务 7 / 任务 9 全部联调通过。同时把这一限制写成注释保留在清单文件里，"
     "便于答辩时说明取舍。"),

    ("问题 5　退出页面后 Logcat 报动态广播接收器泄漏",
     "反复进出广播演示页后，Logcat 出现 IntentReceiver leak 相关警告，"
     "严重时 Activity 销毁时抛异常。",
     "排查发现网络监听是用 registerReceiver 动态注册的，注册后没有成对调用 unregisterReceiver。"
     "动态注册的接收器随组件存活，若不注销，Activity 销毁后系统仍持有引用，即内存泄漏。",
     "在 onDestroy 中调用 unregisterReceiver，并用 registered 布尔标志防止重复注销导致崩溃。",
     "反复进出页面不再出现泄漏警告，广播功能本身不受影响。后续所有动态注册的地方都按此模式处理。"),

    ("问题 6　SQLite 增加字段后表结构没有变化",
     "给 Contact 增加了 gender 字段、并在建表语句里补上该列，但运行后插入数据时报 "
     "table contact has no column named gender。",
     "原因是 SQLiteOpenHelper 的 onCreate 只在数据库文件首次创建时执行一次，"
     "已经存在的 contact.db 不会重新建表，所以新加的列不会生效。",
     "把 VERSION 从 1 提升到 2，并在 onUpgrade 中用 ALTER TABLE contact ADD COLUMN gender TEXT "
     "做增量升级，保证已有数据不丢失。",
     "重装运行后 gender 列存在，增删改查正常；之后再改表结构只要提升版本号即可，"
     "不再需要卸载 App。"),
]

for title_text, phenomenon, reason, fix, result in issues:
    h3(doc, title_text)
    for label, content in (("现象：", phenomenon), ("排查思路：", reason),
                           ("解决方法：", fix), ("整改结果：", result)):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.3)
        p.paragraph_format.space_after = Pt(3)
        style_run(p.add_run(label), size=11, bold=True, font=HEI)
        style_run(p.add_run(content), size=11)

page_break(doc)

# ================================================================ 四
h1(doc, "四、AI 使用记录")

h2(doc, "4.1 使用原则")
para(doc, "全程遵守「AI 辅助、人脑主导」：AI 只用于生成基础配置、通用片段、接口模板与注释，"
          "生命周期、事务、权限、路由这类关键逻辑坚持自己写、自己讲得清。"
          "AI 输出一律先读、再改、后测，不整段粘贴。")

h2(doc, "4.2 使用场景与提示词要点")
table(doc,
      ["序号", "使用场景", "提示词要点", "AI 输出的问题", "人工修正"],
      [
          ["1", "环境排错",
           "描述 Gradle 报 non-ASCII 路径，附完整报错文本",
           "建议「把工程移到纯英文路径」，没有直接给出开关",
           "改用官方开关 android.overridePathCheck，避免搬迁工程"],
          ["2", "代码生成",
           "用 Java 写 RecyclerView 适配器，List 数据源，要求 ViewHolder + 点击回调 + 中文注释",
           "onCreateViewHolder 里 inflate 传了 true",
           "改为 false，否则子项丢失 LayoutParams 导致布局错乱"],
          ["3", "代码审查",
           "审查这段 SQLite DAO 是否存在注入、Cursor 泄漏、事务遗漏",
           "正确指出拼接 SQL 的注入风险，但没提 Cursor 未关闭",
           "补齐 try-with-resources，并补上事务的 setTransactionSuccessful"],
          ["4", "网络封装",
           "封装 HttpURLConnection 工具类，要求回调更新 UI",
           "直接在请求线程里调用回调，未切回主线程",
           "加入 Handler(Looper.getMainLooper()) 统一切主线程"],
          ["5", "后端集成",
           "Spring Boot + MyBatis 工程如何加载 resources/mapper 下的 XML",
           "只说了 @MapperScan，没提 mapper-locations",
           "补充 mapper-locations 配置，修复 Invalid bound statement"],
          ["6", "文档注释",
           "为以下 Java 方法生成 Javadoc，说明参数、返回值与异常",
           "注释准确，个别术语不统一（如「连接」与「链接」混用）",
           "统一术语后采用，作为代码注释的初稿"],
          ["7", "学习对比",
           "对比 org.json 与 Gson 解析 JSON 的优缺点，用表格输出",
           "结论偏泛，缺具体适用边界",
           "结合自己实测补上「结构简单用 org.json、字段多用 Gson」的判断依据"],
      ],
      widths=[1.0, 2.2, 4.6, 3.4, 4.8], font_size=8.5)

h2(doc, "4.3 AI 代码修正清单")

h3(doc, "修正 1　网络请求在主线程执行")
para(doc, "原代码（AI 生成）：", indent=False, bold=True, space_after=1)
code_block(doc,
           'public static String get(String url) throws Exception {\n'
           '    HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();\n'
           '    BufferedReader reader = new BufferedReader(\n'
           '            new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));\n'
           '    StringBuilder sb = new StringBuilder();\n'
           '    String line;\n'
           '    while ((line = reader.readLine()) != null) {\n'
           '        sb.append(line);\n'
           '    }\n'
           '    return sb.toString();\n'
           '}')
para(doc, "问题：方法同步执行且没有起子线程，在 Activity 里直接调用会抛 "
          "NetworkOnMainThreadException；同时没有超时设置，网络差时会一直卡住；"
          "异常直接往上抛，调用方没有统一处理入口。", indent=True)
para(doc, "修正后（节选，完整实现见 HttpUtil.java）：", indent=False, bold=True, space_after=1)
code_block(doc,
           'public static void get(String url, Callback callback) {\n'
           '    request("GET", url, null, callback);\n'
           '}\n'
           '\n'
           'private static void request(final String method, final String url,\n'
           '                            final String jsonBody, final Callback callback) {\n'
           '    new Thread(() -> {                    // 子线程执行\n'
           '        HttpURLConnection conn = null;\n'
           '        try {\n'
           '            conn = (HttpURLConnection) new URL(url).openConnection();\n'
           '            conn.setConnectTimeout(5000);  // 超时保护\n'
           '            conn.setReadTimeout(5000);\n'
           '            int code = conn.getResponseCode();\n'
           '            final String body = readAll(code >= 200 && code < 300\n'
           '                    ? conn.getInputStream() : conn.getErrorStream());\n'
           '            if (code >= 200 && code < 300) {\n'
           '                MAIN.post(() -> callback.onSuccess(body));   // 切主线程\n'
           '            } else {\n'
           '                MAIN.post(() -> callback.onError("HTTP " + code + "：" + body));\n'
           '            }\n'
           '        } catch (Exception e) {\n'
           '            final String msg = e.getClass().getSimpleName() + "：" + e.getMessage();\n'
           '            MAIN.post(() -> callback.onError(msg));\n'
           '        } finally {\n'
           '            if (conn != null) conn.disconnect();\n'
           '        }\n'
           '    }).start();\n'
           '}')

h3(doc, "修正 2　DAO 用字符串拼接 SQL")
para(doc, "原代码（AI 生成）：", indent=False, bold=True, space_after=1)
code_block(doc,
           'public List<Contact> query(String keyword) {\n'
           '    String sql = "SELECT * FROM contact WHERE name LIKE \'%" + keyword + "%\'";\n'
           '    Cursor cursor = db.rawQuery(sql, null);\n'
           '    List<Contact> list = new ArrayList<>();\n'
           '    while (cursor.moveToNext()) {\n'
           '        list.add(read(cursor));\n'
           '    }\n'
           '    return list;            // 没有 close，Cursor 泄漏\n'
           '}')
para(doc, "问题：三个问题叠加。第一，关键字直接拼进 SQL，输入 \' OR \'1\'=\'1 即可绕过条件，存在注入风险；"
          "第二，Cursor 未关闭，反复查询会耗尽游标资源；第三，返回前没有判空处理。", indent=True)
para(doc, "修正后（完整实现见 ContactDao.java）：", indent=False, bold=True, space_after=1)
code_block(doc,
           'public List<Contact> query(String keyword) {\n'
           '    SQLiteDatabase db = helper.getReadableDatabase();\n'
           '    List<Contact> list = new ArrayList<>();\n'
           '\n'
           '    String selection = null;\n'
           '    String[] args = null;\n'
           '    if (keyword != null && !keyword.trim().isEmpty()) {\n'
           '        selection = "name LIKE ?";                          // 参数化占位\n'
           '        args = new String[]{"%" + keyword.trim() + "%"};      // 关键字只作为参数\n'
           '    }\n'
           '\n'
           '    try (Cursor cursor = db.query("contact", null, selection, args,\n'
           '            null, null, "id DESC")) {                        // 自动关闭 Cursor\n'
           '        while (cursor.moveToNext()) {\n'
           '            Contact c = new Contact();\n'
           '            c.setId(cursor.getLong(cursor.getColumnIndexOrThrow("id")));\n'
           '            c.setName(cursor.getString(cursor.getColumnIndexOrThrow("name")));\n'
           '            list.add(c);\n'
           '        }\n'
           '    }\n'
           '    return list;\n'
           '}')

h3(doc, "修正 3　RecyclerView 适配器 inflate 参数错误")
para(doc, "原代码（AI 生成）：", indent=False, bold=True, space_after=1)
code_block(doc,
           '@NonNull\n'
           '@Override\n'
           'public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {\n'
           '    // 第三个参数传 true\n'
           '    View v = LayoutInflater.from(parent.getContext())\n'
           '            .inflate(R.layout.item_contact, parent, true);\n'
           '    return new VH(v);\n'
           '}')
para(doc, "问题：attachToRoot 传 true 会让子项立即被挂到父布局上，"
          "同时返回的 View 会丢失外层 LayoutParams，运行后表现为子项宽度异常、"
          "间距错乱，甚至抛 IllegalStateException。RecyclerView 的 ViewHolder "
          "只负责持有一份视图，挂载由 RecyclerView 自己完成。", indent=True)
para(doc, "修正后：", indent=False, bold=True, space_after=1)
code_block(doc,
           '@NonNull\n'
           '@Override\n'
           'public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {\n'
           '    // 第三个参数必须为 false：由 RecyclerView 负责挂载\n'
           '    View v = LayoutInflater.from(parent.getContext())\n'
           '            .inflate(R.layout.item_contact, parent, false);\n'
           '    return new VH(v);\n'
           '}')

h2(doc, "4.4 AI 使用占比与合规声明")
bullet(doc, "AI 参与部分约占代码总量的 30%，集中在 Gradle 配置、布局骨架、"
            "实体类与注释初稿；生命周期、事务、权限、Provider、分页这些关键逻辑为自己编写。", size=11.5)
bullet(doc, "AI 生成内容全部逐行阅读并本地运行验证，共修正 7 处问题（见 4.2 表与 4.3 清单）。", size=11.5)
bullet(doc, "未向 AI 提供任何真实个人信息、账号口令或数据库数据；"
            "实验中出现的数据库口令仅用于本机教学环境，不写入报告与提交记录。", size=11.5)
bullet(doc, "AI 交互记录与修正过程保留在本报告中，作为作业原创性的核查依据。", size=11.5)

page_break(doc)

# ================================================================ 五
h1(doc, "五、实验总结")

h2(doc, "5.1 知识点收获")
for t in [
    "组件层：理清了 Activity 七大生命周期的触发条件，尤其是 onPause 与 onStop 的分界；"
    "掌握了 Intent 显式与隐式的差别、Bundle 的类型化取值、以及结果回传必须走结果 API。",
    "启动模式：通过实测对比四种 launchMode，理解了任务栈的实际变化，"
    "而不是停留在背概念——singleTask 会清空其上的实例这一点，只有真跑一遍才记得住。",
    "UI 层：四种布局各有适用场景，ConstraintLayout 用约束替代嵌套是降低层级的关键；"
    "RecyclerView 的 ViewHolder 复用机制比 ListView 的 convertView 更彻底。",
    "广播：动态注册要成对注销，静态注册在 Android 8.0 后受隐式广播限制，"
    "有序广播的 priority 决定顺序且可截断。",
    "持久化：文件、SharedPreferences、SQLite 三者不是替代关系而是分工关系；"
    "SQLite 的表结构变更必须靠 onUpgrade 增量迁移，参数化查询是防注入的根本。",
    "权限与 Provider：危险权限必须运行时申请，ContentProvider 把数据访问统一成 URI，"
    "权限管控可以精确到读写。",
    "网络：主线程不能做网络请求，回调必须切回主线程；JSON 解析两种方式各有取舍。",
    "Service：启动式与绑定式解决的是不同问题，一个要活得久，一个要能通信。",
    "工程化：Git 按任务提交、依赖与产物用 .gitignore 隔离、"
    "配置与代码分离，这些习惯比单个知识点更长期有用。",
]:
    bullet(doc, t, size=11.5)

h2(doc, "5.2 Android 原生开发的难点")
numbered(doc, "生命周期是隐式契约。同一个界面在不同操作路径下回调顺序不同，"
              "状态保存、资源释放、线程回调都必须挂在正确的时机上，写错了往往只在特定路径下崩溃。")
numbered(doc, "线程模型容易踩坑。网络、数据库、大文件都不能在主线程做，"
              "而 UI 只能在主线程更新，切换点一多就容易漏。")
numbered(doc, "版本适配成本高。明文 HTTP、静态广播、后台服务、通知权限，"
              "每个版本都收紧一点，同一份代码在不同 API 上行为不同。")
numbered(doc, "资源与引用管理琐碎。Cursor、MediaPlayer、动态广播、ServiceConnection、"
              "Handler 都要成对释放，任何一个漏了都是慢性问题。")
numbered(doc, "前后端联调定位困难。同一个 404 或连接拒绝，可能来自地址、端口、防火墙、"
              "协议、序列化任意一环，必须靠先分测再联调的办法收敛范围。")

h2(doc, "5.3 AI 辅助开发的体会与改进方向")
para(doc, "体会一：AI 在「有明确规格的样板代码」上效率极高，比如 Gradle 配置、"
          "实体类、布局骨架、注释初稿，这些内容正确性容易验证，省下来的时间可以放在逻辑设计上。")
para(doc, "体会二：AI 在「有隐含约束的地方」容易出错。它给出的网络工具类功能是完整的，"
          "但漏掉了线程模型；给出的适配器写法看起来没问题，但 inflate 参数是错的。"
          "这些错误不会让编译失败，只会在运行期表现为卡顿、错位或异常，正是最需要人来把关的地方。")
para(doc, "体会三：让 AI 做「审查」比做「生成」更划算。把已有代码交给它逐条列出风险，"
          "它的覆盖面往往比我自己的检查更全，代价是我必须能判断它说的对不对。")
para(doc, "改进方向：一是建立自己的检查清单，"
          "把线程、生命周期、资源释放、权限、注入这几类高频问题固化成提交前必查项；"
          "二是把 AI 的产出当作初稿而不是答案，凡是涉及并发、状态、安全的部分一律自己重写；"
          "三是保留交互与修正记录，既能复盘，也是原创性的证明。")

h2(doc, "5.4 思考题解答")

h3(doc, "任务 1")
qa("Android 系统四层架构分别是什么？各层职责是什么？",
   "自下而上为：Linux 内核层，负责进程与内存管理、驱动、电源等底层能力；"
   "系统运行库与运行时层，包含 C/C++ 库与 ART 虚拟机，提供图形、数据库、媒体等基础能力；"
   "应用框架层，向开发者暴露 ActivityManager、PackageManager、ContentProvider 等 Java API；"
   "应用层，即我们编写的 App。分层的目的在于每层只依赖下层，硬件差异被内核与运行库屏蔽，"
   "上层接口保持稳定，所以同一份应用代码可以运行在不同厂商的设备上。")
qa("Log.v / d / i / w / e 五个级别分别适用于什么场景？生产环境应如何取舍？",
   "v 用于最细粒度的追踪，只在本地排查时临时打开；d 用于开发期的一般调试信息；"
   "i 用于关键流程节点，如页面进入、登录成功、接口返回等；"
   "w 用于可恢复的异常情况，如数据为空、重试成功；e 用于已发生的错误但还未崩溃。"
   "生产环境应关闭 v 与 d，保留 i 记录关键链路、w 与 e 用于问题定位，"
   "并避免在日志里打印用户隐私与口令。")

h3(doc, "任务 2")
qa("什么业务场景必须使用 singleTask？为什么？",
   "典型是全局唯一的主界面或入口页，例如应用主页、扫码页、IM 的会话列表。"
   "这类页面在整个任务栈中只应存在一个实例：用 singleTask 后，无论从哪个页面再次打开，"
   "系统都会复用已有实例并把它之上的页面清掉，避免用户返回时看到重复页面，"
   "也避免同一份数据在多个实例里不同步。它同时还能配合 onNewIntent 处理新的跳转参数。")
qa("onPause 与 onStop 何时都会执行、何时只执行 onPause？",
   "当当前界面被完全遮挡时两者都会执行：先 onPause 再 onStop。"
   "当界面只是部分失去焦点、仍然可见时，只执行 onPause，例如弹出对话框主题的 Activity、"
   "或者分屏、悬浮窗场景。核心判断标准是「界面是否还可见」，"
   "因此耗时资源释放应放在 onStop，而轻量的状态保存放 onPause。")

h3(doc, "任务 3")
qa("RecyclerView 相比 ListView 有哪些优势？",
   "一是强制 ViewHolder，复用机制更彻底，滑动更流畅；"
   "二是布局与职责解耦，通过 LayoutManager 一行代码在列表、网格、瀑布流之间切换；"
   "三是支持局部刷新，notifyItemChanged 等精确到位置的更新方法，避免整表重绘；"
   "四是动画内置，增删改自带过渡效果；五是支持 ItemDecoration、ItemAnimator 等扩展点。"
   "ListView 只支持垂直列表，且局部刷新能力弱。")
qa("如何减少布局嵌套层级？过度绘制会带来什么后果？",
   "手段包括：用 ConstraintLayout 通过约束替代多层 LinearLayout；"
   "用 merge 标签减少无意义的父节点；用 include 复用公共布局；"
   "能用一个 TextView 加 span 表达的就不要用多个叠起来；避免 background 层层叠加。"
   "过度绘制的后果是同一片像素被重复绘制，导致滑动掉帧、耗电增加、低端设备卡顿。"
   "可以用开发者选项里的「显示过度绘制」和 Layout Inspector 检查层级与重绘区域。")

h3(doc, "任务 4")
qa("普通广播与有序广播的区别是什么？",
   "普通广播（sendBroadcast）的接收器之间没有顺序，按注册情况并发投递，彼此收不到对方的结果，"
   "效率高但不保证顺序。有序广播（sendOrderedBroadcast）按 priority 从高到低依次投递，"
   "前一个接收器可以修改结果数据，也可以用 abortBroadcast 截断，后续接收器不再收到，"
   "因此适合需要按优先级处理或需要终止的场景，代价是串行执行、效率较低。")
qa("为什么 Android 8.0 之后限制静态注册？如何适配？",
   "静态注册的接收器会随系统广播被唤醒，应用即使没运行也会被拉起，"
   "大量应用监听隐式广播造成频繁唤醒、耗电和卡顿，这些广播多数与用户当前操作无关。"
   "因此 8.0 对多数隐式广播禁止静态注册，仅保留少数例外。"
   "适配方式：一是改为动态注册，把注册放在 onStart 或 onCreate、注销放在 onStop 或 onDestroy；"
   "二是发送方用 setPackage 或显式 Intent 把广播限定到目标包，"
   "这类定向广播可以绕过限制；三是改用 JobScheduler 或 WorkManager 处理后台任务。")

h3(doc, "任务 5")
qa("三种持久化方案各适合什么场景？",
   "文件存储适合内容较大的非结构化数据，如文本笔记、图片、缓存文件；"
   "SharedPreferences 适合少量键值对配置，如登录状态、主题、记住密码，"
   "本质是一个 XML，不适合存大量或结构化数据；"
   "SQLite 适合结构化、需要按条件查询与关联的数据，如通讯录、订单，支持事务与索引。"
   "选择原则是先看数据有没有结构，再看数据量和查询需求。")
qa("commit 与 apply 有何区别？事务不加 setTransactionSuccessful 会怎样？",
   "commit 同步写入磁盘并返回 boolean 表示成功与否，会阻塞调用线程；"
   "apply 先改内存再异步落盘，无返回值，不阻塞主线程。"
   "UI 线程优先用 apply，需要在写入后立刻读取结果或必须确认成功时才用 commit。"
   "事务结束后如果不调用 setTransactionSuccessful，endTransaction 会执行回滚，"
   "事务中的所有写操作全部作废且不报错，数据看起来「莫名没写进去」。")

h3(doc, "任务 6")
qa("普通权限与危险权限的区别？为什么要运行时申请？",
   "普通权限只涉及应用自身的数据或极低风险能力，如网络访问、Wi-Fi 状态，"
   "在清单里声明即自动授予。危险权限涉及用户隐私或设备能力，如通讯录、相机、定位、存储，"
   "必须运行时向用户申请。之所以改为运行时申请，是因为安装时一次性授权用户无法判断风险，"
   "一旦授予就长期有效；运行时申请让授权发生在真正用到该能力的时刻，"
   "用户可以结合上下文决定是否同意，也可以事后在设置中撤销，符合最小必要原则。")
qa("ContentProvider 相比直接暴露文件或数据库有什么优势？",
   "一是统一入口，调用方只依赖 URI，不关心底层是 SQLite、文件还是网络；"
   "二是权限可控，可以分别设置 readPermission 与 writePermission，"
   "还能通过 grantUriPermission 做临时授权，而直接暴露文件路径几乎无法细粒度管控；"
   "三是跨进程安全，由系统的 Binder 机制与 ContentResolver 代理负责 IPC，"
   "开发者不用自己实现序列化与进程通信；四是支持数据变化通知（notifyChange / ContentObserver）。")

h3(doc, "任务 7")
qa("为什么 Android 禁止主线程网络请求？",
   "主线程同时承担 UI 绘制与输入事件处理。网络请求耗时不可预测，"
   "一旦在主线程阻塞，界面就无法刷新、点击无响应，超过约 5 秒就会 ANR。"
   "系统用 NetworkOnMainThreadException 强制拦截，本质上是在保护可用性。"
   "正确做法是把网络放到子线程或线程池，结果通过 Handler 或 runOnUiThread 切回主线程更新 UI。")
qa("Gson 与 org.json 各自的适用场景是什么？",
   "org.json 是 Android 内置库，逐字段取值，零依赖、体积小，"
   "适合结构简单、只取少数字段的场景，或者需要动态判断结构的情况；"
   "Gson 通过反射把 JSON 一次性映射成实体对象，代码量少、可读性好，"
   "适合结构稳定、字段较多、需要嵌套对象的场景，代价是引入依赖且有反射开销。"
   "本实验用两者解析同一份数据，实测结论是字段少时 org.json 更直接，"
   "字段多或需要传给业务层时 Gson 明显省事。")

h3(doc, "任务 8")
qa("启动式与绑定式 Service 分别适用什么场景？",
   "启动式（startService）启动后与调用方没有连接关系，即使调用方退出服务仍可运行，"
   "适合后台任务，如下载、播放音乐，但调用方无法直接调用服务的方法，只能靠广播或回调通信。"
   "绑定式（bindService）通过 Binder 建立连接，调用方可以直接调用服务的方法，"
   "所有绑定方解绑后服务自动销毁，适合需要交互的场景，如音乐播放器的播放控制、"
   "实时数据查询。二者也可以同时使用。")
qa("Android 8.0 之后为什么限制后台服务？有哪些替代方案？",
   "原因是后台服务长期占用资源并频繁唤醒，用户看不到却耗电，很多应用借此常驻后台。"
   "8.0 起对后台启动服务做了限制，应用进入后台后一段时间内必须停止普通服务，否则抛异常。"
   "替代方案：需要用户感知的长时间任务改用前台服务并 startForeground 显示通知；"
   "可延迟的任务用 JobScheduler 或 WorkManager，由系统在合适时机统一调度；"
   "短时任务用协程或线程池配合生命周期管理。")

h3(doc, "任务 9")
qa("梳理一次完整的 App 请求到界面渲染的链路。",
   "以员工列表为例：EmpListActivity 调用 HttpUtil.get，在子线程用 HttpURLConnection "
   "向 http://10.0.2.2:8080/api/emps?page=1&size=5 发起请求；"
   "请求经模拟器的 10.0.2.2 映射到宿主机的 Spring Boot；"
   "EmpController 接收参数交给 EmpService；Service 把页码换算成 offset，"
   "调用 EmpMapper.findPage；MyBatis 按 EmpMapper.xml 生成带 LIMIT/OFFSET 的 SQL 交给 MySQL；"
   "结果集按 map-underscore-to-camel-case 映射成 Emp 对象返回；"
   "Controller 组装 {total,page,size,list} 由 Jackson 序列化为 JSON；"
   "客户端在子线程读到响应字符串，用 Handler 切回主线程；"
   "Gson 解析成 List<Emp>，adapter.notifyDataSetChanged 触发 RecyclerView 重新绑定并绘制。"
   "任何一环出错都会表现为列表为空或报错，所以排查要按这个顺序逐段验证。")
qa("对比 Android 原生与后续将学的 UniApp 实现同一列表页的开发效率。",
   "从本实验的实际体验推断：原生要实现同一列表页，需要写布局 XML、item 布局、"
   "Adapter 与 ViewHolder、网络工具类、实体类、JSON 解析、分页逻辑，"
   "代码量大约在 300 到 400 行，好处是性能可控、能直接访问系统能力。"
   "UniApp 用 template 加 v-for 就能完成列表渲染，网络请求是 uni.request 一个 API，"
   "同样的页面代码量可能只有三分之一，且一次编写可发布到 H5、小程序、App 多端。"
   "但代价是复杂原生能力需要插件或封装、极端性能场景不如原生、"
   "部分平台差异仍需条件编译处理。结论是业务型页面选跨端更划算，"
   "重交互或重性能的模块仍应原生实现。")

page_break(doc)

# ================================================================ 附录
h1(doc, "附录　截图清单与提交物")

para(doc, "报告正文中的截图占位框与下表一一对应，按编号补齐后删除占位框即可。")

table(doc,
      ["图号", "所属任务", "截图内容"],
      [
          ["图 1", "任务1", "Logcat 五级日志输出"],
          ["图 2", "任务1", "Project 目录结构"],
          ["图 3", "任务2", "SecondActivity 接收到的参数"],
          ["图 4", "任务2", "结果回传后的 FirstActivity"],
          ["图 5", "任务2", "生命周期日志序列"],
          ["图 6", "任务3", "登录页（四种布局与常用控件）"],
          ["图 7", "任务3", "RecyclerView 联系人列表"],
          ["图 8", "任务3", "简易聊天室界面"],
          ["图 9", "任务4", "网络变化广播"],
          ["图 10", "任务4", "有序广播投递顺序"],
          ["图 11", "任务5", "文件存储与 SharedPreferences"],
          ["图 12", "任务5", "SQLite 通讯录列表"],
          ["图 13", "任务5", "事务批量插入结果"],
          ["图 14", "任务6", "运行时权限申请弹窗"],
          ["图 15", "任务6", "自定义 ContentProvider 查询结果"],
          ["图 16", "任务7", "org.json 与 Gson 解析结果"],
          ["图 17", "任务7", "POST 新增用户与异常兜底"],
          ["图 18", "任务8", "Service 生命周期日志"],
          ["图 19", "任务8", "定位与多媒体"],
          ["图 20", "任务9", "员工列表（分页）"],
          ["图 21", "任务9", "新增与修改员工"],
          ["图 22", "任务9", "数据库一致性核对"],
      ],
      widths=[1.8, 2.6, 11.6], font_size=9.5)

h2(doc, "提交物清单")
for t in [
    "实验报告（本文件，Word 或 PDF）。",
    "Android 客户端源码：HelloAndroid（31 个 Java 类、17 个布局文件）。",
    "后端源码：AndroidLabServer（Spring Boot + MyBatis + MySQL）。",
    "数据库脚本：AndroidLabServer/sql/init.sql。",
    "可运行安装包：HelloAndroid/app/build/outputs/apk/debug/app-debug.apk。",
    "Git 仓库：https://github.com/Ogsting/Android1（main 分支，按任务 1 到 9 分次提交）。",
]:
    bullet(doc, t, size=11.5)

doc.save(OUT)
print("saved:", os.path.abspath(OUT))
