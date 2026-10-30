# -*- coding: utf-8 -*-
"""生成《实验一 实验步骤指导》。

正文中的引用统一用「」，避免与 Python 字符串定界符冲突。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.shared import Cm, Pt
from docx_kit import (bullet, code_block, h1, h2, h3, new_document, note,
                      numbered, page_break, para, style_run, table, title)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "实验一_实验步骤指导.docx")

doc = new_document("实验一 实验步骤指导")

title(doc, "《移动应用开发（AI 赋能版）》", "实验一 实验步骤指导")
para(doc, "AI 赋能 Android 原生开发综合实验　|　24 学时　|　个人独立完成　|　9 个任务",
     size=11, indent=False, align="center")

note(doc, "使用说明：本文档是照着做的操作手册，按任务 1 到 9 的顺序执行。"
          "每完成一个任务就按文中提示截一次图、做一次 Git 提交——截图与提交都是评分项，"
          "缺一项就会扣分。配套代码在 HelloAndroid（客户端）与 AndroidLabServer（后端）两个目录。")

# ============================================================ 一、环境核对
h1(doc, "一、开工前的环境核对")

para(doc, "本机已实测通过的环境如下，先用 3 分钟确认一遍，避免后面浪费时间排错。")

table(doc,
      ["组件", "本机实际值", "核对方式"],
      [
          ["JDK", "21.0.8（D:\\java\\jdk.21）", "命令行执行 java -version"],
          ["Android SDK", "D:\\Android\\Sdk（Platform 34、Build-Tools 34.0.0）",
           "Android Studio 的 SDK Manager"],
          ["Gradle", "8.7（项目内 gradlew 自动下载）", "gradlew.bat -v"],
          ["AGP", "8.4.2", "见 build.gradle 插件版本"],
          ["MySQL", "8.0.46，端口 3306，服务已启动", "服务里看 MySQL80 是否 Running"],
          ["Maven", "3.9.9（D:\\tools\\apache-maven-3.9.9）", "mvn -version"],
          ["Git", "D:\\Git\\Git\\cmd\\git.exe", "git --version"],
          ["模拟器", "Pixel_API_34（AVD 位于 D:\\Android\\Avd）", "Device Manager 中可见"],
      ],
      widths=[3.0, 7.6, 5.6], first_col_bold=True)

h2(doc, "1.1 必须知道的三个坑")
numbered(doc, "工程目录含中文（D:\\HOMEWORK\\HomeWork\\安卓）。AGP 默认会直接报错拒绝构建，"
              "已在 gradle.properties 中加 android.overridePathCheck=true 放行；"
              "同时 compileOptions 里强制 UTF-8，否则中文注释会变乱码。")
numbered(doc, "模拟器访问电脑上的后端不能用 localhost。localhost 指向模拟器自身，"
              "必须用 10.0.2.2（已写在 network/ApiConfig.java）。真机调试改成电脑的局域网 IP。")
numbered(doc, "Android 9.0 起默认禁止明文 HTTP。AndroidManifest.xml 里已加 "
              "android:usesCleartextTraffic 为 true，这是实验联调必需的，"
              "生产环境应改用 HTTPS——这一点答辩常被问，要能说清楚。")

# ============================================================ 二、四步起跑
h1(doc, "二、四个启动步骤（做完再进任务）")

h2(doc, "步骤 1：初始化数据库")
para(doc, "在项目根目录 D:\\HOMEWORK\\HomeWork\\安卓 打开命令行，执行：")
code_block(doc,
           'mysql -u root -p --default-character-set=utf8mb4 < AndroidLabServer\\sql\\init.sql',
           caption="初始化 android_lab 库")
para(doc, "执行完应看到 user_count=4、emp_count=7。若命令行里 source 中文路径报 "
          "Failed to open file，说明是路径含中文导致，把 init.sql 复制到 C:\\Temp 再执行，"
          "或用 Navicat / Workbench 直接打开运行。")

note(doc, "库里用的是新建的 android_lab，不是之前的 ssm_emp。两者表结构一致，"
          "这样实验里的增删改不会破坏原有课程数据；报告里可以写成复用先修课表结构的合理做法。")

h2(doc, "步骤 2：启动后端并自测")
code_block(doc,
           'cd AndroidLabServer\n'
           'mvn -DskipTests package\n'
           'set MYSQL_PASSWORD=你的MySQL口令\n'
           'java -jar target\\android-lab-server-1.0.0.jar',
           caption="编译并启动 Spring Boot 后端（口令走环境变量，不写进配置文件）")
para(doc, "看到 Started LabServerApplication 即成功，端口 8080。再开一个命令行自测：")
code_block(doc,
           'curl http://localhost:8080/api/users\n'
           'curl "http://localhost:8080/api/emps?page=1&size=5"',
           caption="自测两个查询接口（PowerShell 用 curl.exe 或 Invoke-RestMethod）")
para(doc, "两个接口都返回中文正常的 JSON 才算通。任务 7 和任务 9 依赖它，务必先跑通。")

h2(doc, "步骤 3：编译 APK")
code_block(doc,
           'cd HelloAndroid\n'
           'gradlew.bat assembleDebug',
           caption="编译 Debug 包")
para(doc, "首次编译要下载依赖，5 到 15 分钟属正常。产物在 "
          "app\\build\\outputs\\apk\\debug\\app-debug.apk（本机约 5.7 MB）。")

h2(doc, "步骤 4：启动模拟器并安装")
para(doc, "Android Studio 的 Device Manager 里启动 Pixel_API_34；模拟器就绪后：")
code_block(doc,
           'adb install -r app\\build\\outputs\\apk\\debug\\app-debug.apk\n'
           'adb shell am start -n com.example.helloandroid/.MainActivity',
           caption="安装并启动 App")
para(doc, "也可以直接在 Android Studio 里点运行按钮。启动后是任务导航页，"
          "9 个任务的入口都在上面。")

page_break(doc)

# ============================================================ 三、任务 1~9
h1(doc, "三、任务 1~9 操作步骤")

# ---------------- 任务 1
h2(doc, "任务 1　开发环境与 Log 调试（2 学时）")
h3(doc, "实验目标")
para(doc, "验证 JDK、SDK、Gradle、模拟器整条链路可用，掌握项目目录结构与 Log 五级日志的用途。")
h3(doc, "操作步骤")
numbered(doc, "Android Studio 里 File 到 Open，选择 D:\\HOMEWORK\\HomeWork\\安卓\\HelloAndroid，"
              "等待 Gradle Sync 完成（Build 窗口显示 BUILD SUCCESSFUL）。")
numbered(doc, "展开左侧 Project 视图，逐层查看：app/src/main/java（源码）、res/layout（布局）、"
              "res/values（字符串与主题）、AndroidManifest.xml（清单）。")
numbered(doc, "启动模拟器，点 Run 把 App 运行起来。")
numbered(doc, "打开底部 Logcat，过滤框输入 tag:HelloAndroid，日志级别选 Verbose。")
numbered(doc, "确认能看到 V、D、I、W、E 五条日志（对应 MainActivity.onCreate 里的五行 Log 调用）。")
numbered(doc, "命令行再补两个验证：java -version、sdkmanager --list。")
h3(doc, "要截的图")
bullet(doc, "截图 1：Logcat 过滤 tag:HelloAndroid 后的 V/D/I/W/E 五条日志，含时间戳与进程号。")
bullet(doc, "截图 2：Android Studio 左侧 Project 目录树展开到 res/layout 的样子。")
h3(doc, "Git 提交")
code_block(doc, 'git add . && git commit -m "feat(任务1): 环境搭建与 Log 五级日志输出"')

# ---------------- 任务 2
h2(doc, "任务 2　Activity 生命周期与 Intent 页面通信（3 学时）")
h3(doc, "实验目标")
para(doc, "掌握七大生命周期回调的触发时机，掌握 Intent 显式与隐式跳转、Bundle 传参与结果回传，"
          "理解四种启动模式对任务栈的影响。")
h3(doc, "操作步骤")
numbered(doc, "首页点任务2 入口，进入 FirstActivity。")
numbered(doc, "点显式 Intent 跳转并传参，SecondActivity 上应显示 username 为张三、age 为 20、"
              "isVip 为 true。")
numbered(doc, "点回传结果并 finish，返回 FirstActivity，应显示「收到回传：欢迎 张三」。")
numbered(doc, "按 Home 键回到桌面，再从最近任务进入，在 Logcat 观察 "
              "onPause、onStop、onRestart、onStart、onResume 的顺序。")
numbered(doc, "在模拟器右侧工具栏点旋转按钮，观察 Activity 被销毁重建，即 onDestroy 后重新 onCreate。")
numbered(doc, "打开 AndroidManifest.xml，把 SecondActivity 的 launchMode 依次改成 "
              "standard、singleTop、singleTask、singleInstance，每次改完重装运行，"
              "在 SecondActivity 里点再次启动本页，对比 Logcat 中 onCreate 出现的次数。")
numbered(doc, "点隐式 Intent 打开系统浏览器，体会隐式 Intent 由系统匹配处理者的差别。")
h3(doc, "要截的图")
bullet(doc, "截图 3：SecondActivity 显示三个传入参数值的界面。")
bullet(doc, "截图 4：FirstActivity 显示「收到回传：欢迎 张三」。")
bullet(doc, "截图 5：Logcat 中完整的一次生命周期序列；建议再截一张 singleTask 与 standard 的差异对比。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务2): 生命周期日志、Intent 传参与回传、四种启动模式对比"')

# ---------------- 任务 3
h2(doc, "任务 3　UI 布局与常用控件（3 学时）")
h3(doc, "实验目标")
para(doc, "掌握 LinearLayout、RelativeLayout、FrameLayout、ConstraintLayout 四种布局，"
          "掌握 7 种以上控件的取值赋值与事件处理，能独立完成 RecyclerView 列表与聊天室界面。")
h3(doc, "操作步骤")
numbered(doc, "首页点任务3-1 入口，进入登录页。注意根布局是 LinearLayout，标题区用 FrameLayout 叠加，"
              "按钮区用 RelativeLayout，表单区用 ConstraintLayout——一页覆盖四种布局。")
numbered(doc, "什么都不填直接点登录，应弹出「用户名不能为空」。")
numbered(doc, "填入用户名和密码，切换学生与教师单选、勾选记住密码、打开通知开关，再点登录，"
              "弹出的 Toast 会汇总所有控件的取值。")
numbered(doc, "点清空按钮，观察 EditText 被 setText 置空并重新获得焦点。")
numbered(doc, "返回首页，点任务3-2 入口，进入 RecyclerView 联系人列表，点击任意条目应弹出 Toast。")
numbered(doc, "返回首页，点任务3-3 入口，进入简易聊天室，在底部输入框输入文字后点发送，"
              "新消息应出现在右侧蓝色气泡，原消息在左侧灰色气泡。")
h3(doc, "要截的图")
bullet(doc, "截图 6：登录页完整界面，能看出四种布局区域与 7 种控件。")
bullet(doc, "截图 7：登录成功后的 Toast 汇总信息。")
bullet(doc, "截图 8：RecyclerView 联系人列表。")
bullet(doc, "截图 9：聊天室左右气泡效果，至少两条不同方向的消息。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务3): 四种布局与常用控件、RecyclerView、聊天室界面"')

page_break(doc)

# ---------------- 任务 4
h2(doc, "任务 4　广播机制（2 学时）")
h3(doc, "实验目标")
para(doc, "理解广播的收发模型，掌握动态注册与静态注册的差异，以及有序广播的优先级与截断机制。")
h3(doc, "操作步骤")
numbered(doc, "首页点任务4 入口。")
numbered(doc, "下拉通知栏点飞行模式开关，再回到 App，界面状态文本应变成「网络状态变化：已断开」；"
              "关掉飞行模式应恢复为已连接。")
numbered(doc, "点发送自定义广播，弹出 Toast「静态接收器收到：你好，静态接收器」。"
              "注意代码里调用了 setPackage(getPackageName())，这是绕开 Android 8.0 隐式广播限制的关键。")
numbered(doc, "点发送有序广播，到 Logcat 搜索 OrderedReceiverA 与 OrderedReceiverB，"
              "确认 A（priority 为 100）先执行、B（priority 为 50）后执行，"
              "且 B 打印出了 A 设置的 resultData。")
numbered(doc, "选做：在 OrderedReceiverA 里加一行 abortBroadcast()，重装后再发，B 将收不到。")
h3(doc, "要截的图")
bullet(doc, "截图 10：飞行模式下界面显示「网络状态变化：已断开」。")
bullet(doc, "截图 11：自定义广播的 Toast。")
bullet(doc, "截图 12：Logcat 中有序广播 A 到 B 的执行顺序与 resultData。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务4): 动态/静态广播与有序广播优先级实验"')

# ---------------- 任务 5
h2(doc, "任务 5　数据持久化（4 学时，本实验重点）")
h3(doc, "实验目标")
para(doc, "掌握文件存储、SharedPreferences、SQLite 三种持久化方案，"
          "完成带增删改查与事务的通讯录案例。")
h3(doc, "操作步骤")
numbered(doc, "首页点任务5-1 入口，进入文件存储与 SharedPreferences 页面。")
numbered(doc, "在输入框写一段文字，点写文件，再点读文件，下方应显示刚写入的内容。")
numbered(doc, "点 SharedPreferences 保存，再点读取，应显示 username 与 remember 为 true。")
numbered(doc, "返回首页，点任务5-2 入口，进入 SQLite 通讯录。填入姓名、电话、邮箱，点保存，"
              "列表新增一条，连续添加 3 条。")
numbered(doc, "在按姓名模糊查询框输入姓氏，点查询，列表应只剩匹配项；点全部恢复。")
numbered(doc, "点击列表某一条，数据回填到表单进入编辑模式，改电话后点保存，列表应更新。")
numbered(doc, "长按某一条，确认弹窗点删除，列表应移除。")
numbered(doc, "点事务批量插入 3 条，一次事务插入三条记录，列表刷新。")
numbered(doc, "选做：命令行验证数据库真的落盘，adb shell 进 "
              "/data/data/com.example.helloandroid/databases/，用 sqlite3 查 contact 表。")
h3(doc, "要截的图")
bullet(doc, "截图 13：文件存储读回的内容。")
bullet(doc, "截图 14：SharedPreferences 读取结果。")
bullet(doc, "截图 15：SQLite 通讯录列表，至少 3 条数据。")
bullet(doc, "截图 16：模糊查询结果。")
bullet(doc, "截图 17：事务批量插入后列表变为 6 条以上。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务5): 文件存储、SharedPreferences、SQLite 通讯录 CRUD 与事务"')

# ---------------- 任务 6
h2(doc, "任务 6　内容提供器与运行时权限（2 学时）")
h3(doc, "实验目标")
para(doc, "掌握危险权限的运行时申请流程，理解 ContentResolver 与 ContentProvider 的协作方式。")
h3(doc, "操作步骤")
numbered(doc, "先在模拟器里打开系统通讯录 App，手动添加 2 到 3 个联系人"
              "（模拟器默认是空的，不加会看到通讯录为空）。")
numbered(doc, "回到 App，首页点任务6 入口。")
numbered(doc, "点申请 READ_CONTACTS 并读取系统通讯录，系统弹出权限框，点允许，"
              "下方应列出刚才添加的联系人。")
numbered(doc, "到系统设置里把该 App 的通讯录权限关掉，再点同一按钮并选拒绝，"
              "应提示「权限被拒绝，无法读取通讯录」。")
numbered(doc, "点通过 ContentResolver 查询自定义 Provider，应显示任务 5 里添加的联系人，"
              "说明自定义 ContentProvider 读取的是同一个 SQLite 库。")
h3(doc, "要截的图")
bullet(doc, "截图 18：运行时权限申请弹窗。")
bullet(doc, "截图 19：读取到的系统通讯录列表。")
bullet(doc, "截图 20：通过自定义 ContentProvider 查到的数据。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务6): READ_CONTACTS 运行时权限与自定义 ContentProvider"')

page_break(doc)

# ---------------- 任务 7
h2(doc, "任务 7　网络技术应用（4 学时）")
h3(doc, "实验目标")
para(doc, "掌握 HttpURLConnection 发起 GET 与 POST，掌握 org.json 与 Gson 两种 JSON 解析方式，"
          "完成与 Spring 后端的接口联调。")
h3(doc, "操作步骤")
numbered(doc, "确认后端已启动：浏览器打开 http://localhost:8080/api/users 能看到 JSON。")
numbered(doc, "首页点任务7 入口。")
numbered(doc, "点 GET 请求配合 org.json 解析，界面应列出 4 个用户，格式为 id、昵称与 username。")
numbered(doc, "点 GET 请求配合 Gson 解析，同样 4 条数据，但代码侧用 TypeToken 反序列化。")
numbered(doc, "点 POST 提交 JSON 新增用户，提示 POST 成功并返回带 id 的对象；"
              "到浏览器刷新 /api/users，能看到多出一条。")
numbered(doc, "把后端进程停掉再点 GET，界面应显示请求失败与排查提示，这是网络异常兜底的效果。")
h3(doc, "要截的图")
bullet(doc, "截图 21：org.json 解析结果。")
bullet(doc, "截图 22：Gson 解析结果。")
bullet(doc, "截图 23：POST 新增成功的返回内容，配合浏览器里 /api/users 的新数据。")
bullet(doc, "截图 24：后端未启动时的错误提示界面，体现异常处理。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务7): HttpURLConnection + org.json/Gson 双解析与接口联调"')

# ---------------- 任务 8
h2(doc, "任务 8　后台服务与定位多媒体（2 学时）")
h3(doc, "实验目标")
para(doc, "理解 Service 生命周期与启动式、绑定式的差异，能开发定位与多媒体功能。")
h3(doc, "操作步骤")
numbered(doc, "首页点任务8-1 入口，先打开 Logcat 过滤 tag:MyService。")
numbered(doc, "点 startService 启动服务，Logcat 应依次出现 onCreate 与 onStartCommand（带 startId）。"
              "再点一次，只会重复 onStartCommand，不会再走 onCreate。")
numbered(doc, "点 stopService 停止服务，出现 onDestroy。")
numbered(doc, "点 bindService 绑定服务，出现 onCreate 与 onBind，界面显示 increase() 的返回值；"
              "点 unbindService 解绑，出现 onUnbind 与 onDestroy。")
numbered(doc, "返回首页点任务8-2 入口。先在模拟器右侧工具栏的 Extended controls 里进 Location，"
              "注入一个坐标，例如纬度 39.9、经度 116.4。")
numbered(doc, "点获取一次定位，界面显示经纬度与精度。")
numbered(doc, "点 MediaPlayer 播放网络音频，几秒后应开始播放（模拟器需能联网）。")
numbered(doc, "点调用系统相机拍照，授权相机权限后打开系统相机。")
h3(doc, "要截的图")
bullet(doc, "截图 25：Logcat 中 Service 的 onCreate、onStartCommand、onDestroy 完整序列。")
bullet(doc, "截图 26：绑定服务后 increase() 的返回值。")
bullet(doc, "截图 27：定位得到的经纬度。")
bullet(doc, "截图 28：MediaPlayer 播放状态或相机拍照界面。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务8): Service 双启动方式、定位与多媒体"')

# ---------------- 任务 9
h2(doc, "任务 9　Android 与 SpringMVC 整合（2 学时）")
h3(doc, "实验目标")
para(doc, "完成 App 请求、后端处理、数据库、响应、界面渲染的全链路，"
          "实现员工管理的分页、新增、修改、删除。")
h3(doc, "操作步骤")
numbered(doc, "确认后端与 MySQL 都在运行，访问 /api/emps?page=1&size=5 应返回 7 条数据。")
numbered(doc, "首页点任务9 入口，进入后自动加载第一页，正常应显示 5 条员工与总条数统计。")
numbered(doc, "点加载下一页，列表追加第 6、7 条。")
numbered(doc, "填入姓名、部门、岗位、薪资，点新增，列表会回到第一页并出现新员工。")
numbered(doc, "点击某条员工，弹窗修改岗位，保存后列表刷新为新岗位。")
numbered(doc, "长按某条员工，确认后删除，总数减一。")
numbered(doc, "到 MySQL 里核对数据一致性：")
code_block(doc,
           'mysql -u root -p -e "USE android_lab; SELECT emp_id, emp_name, dept, post FROM emp;"',
           caption="核对数据库里的实际数据")
numbered(doc, "选做：用 Postman 对同一组接口做一遍 CRUD，作为接口正确性的独立验证。")
h3(doc, "要截的图")
bullet(doc, "截图 29：员工列表第一页，含总数统计文字。")
bullet(doc, "截图 30：新增员工后的列表。")
bullet(doc, "截图 31：修改岗位后的效果。")
bullet(doc, "截图 32：删除确认弹窗或删除后的列表。")
bullet(doc, "截图 33：MySQL 中查询到的数据，与 App 显示一致。")
h3(doc, "Git 提交")
code_block(doc, 'git commit -m "feat(任务9): 员工管理 CRUD 前后端全链路联调"')

page_break(doc)

# ============================================================ 四、截图清单
h1(doc, "四、截图清单（共 33 张，建议按此顺序拍）")

para(doc, "报告模板只要求每个任务至少 1 张，但下面这些是能体现完整过程的最小集合。"
          "建议文件名直接用编号，便于回填报告时对号入座。")

table(doc,
      ["编号", "所属任务", "拍摄内容", "建议文件名"],
      [
          ["1", "任务1", "Logcat 五级日志", "01_logcat.png"],
          ["2", "任务1", "Project 目录树", "02_tree.png"],
          ["3", "任务2", "SecondActivity 参数展示", "03_params.png"],
          ["4", "任务2", "回传结果", "04_reply.png"],
          ["5", "任务2", "生命周期日志序列", "05_lifecycle.png"],
          ["6", "任务3", "登录页", "06_login.png"],
          ["7", "任务3", "登录 Toast", "07_toast.png"],
          ["8", "任务3", "RecyclerView 列表", "08_rv.png"],
          ["9", "任务3", "聊天室气泡", "09_chat.png"],
          ["10", "任务4", "网络状态变化", "10_network.png"],
          ["11", "任务4", "自定义广播 Toast", "11_broadcast.png"],
          ["12", "任务4", "有序广播日志", "12_ordered.png"],
          ["13", "任务5", "文件读回", "13_file.png"],
          ["14", "任务5", "SharedPreferences", "14_sp.png"],
          ["15", "任务5", "通讯录列表", "15_db_list.png"],
          ["16", "任务5", "模糊查询", "16_db_search.png"],
          ["17", "任务5", "事务批量插入", "17_db_tx.png"],
          ["18", "任务6", "权限弹窗", "18_perm.png"],
          ["19", "任务6", "系统通讯录", "19_contacts.png"],
          ["20", "任务6", "自定义 Provider 数据", "20_provider.png"],
          ["21", "任务7", "org.json 解析", "21_orgjson.png"],
          ["22", "任务7", "Gson 解析", "22_gson.png"],
          ["23", "任务7", "POST 成功", "23_post.png"],
          ["24", "任务7", "网络异常提示", "24_neterror.png"],
          ["25", "任务8", "Service 日志", "25_service.png"],
          ["26", "任务8", "绑定服务调用", "26_bind.png"],
          ["27", "任务8", "定位结果", "27_location.png"],
          ["28", "任务8", "多媒体播放", "28_media.png"],
          ["29", "任务9", "员工列表", "29_emp_list.png"],
          ["30", "任务9", "新增员工", "30_emp_add.png"],
          ["31", "任务9", "修改员工", "31_emp_edit.png"],
          ["32", "任务9", "删除员工", "32_emp_del.png"],
          ["33", "任务9", "MySQL 数据", "33_mysql.png"],
      ],
      widths=[1.4, 2.4, 7.4, 5.0], font_size=9.5)

# ============================================================ 五、Git 节奏
h1(doc, "五、Git 提交节奏（评分项：每任务至少一次有效提交）")

para(doc, "仓库已初始化并关联 https://github.com/Ogsting/Android1.git，分支为 main，"
          "已按任务 1 到 9 各提交一次。你后续每做完一个任务，补一次提交即可：")

table(doc,
      ["提交时机", "提交说明模板"],
      [
          ["任务 1 完成", "feat(任务1): 环境搭建与 Log 五级日志输出"],
          ["任务 2 完成", "feat(任务2): 生命周期日志、Intent 传参与回传、四种启动模式"],
          ["任务 3 完成", "feat(任务3): 四种布局与常用控件、RecyclerView、聊天室界面"],
          ["任务 4 完成", "feat(任务4): 动态/静态广播与有序广播优先级实验"],
          ["任务 5 完成", "feat(任务5): 三种持久化方案与 SQLite 通讯录 CRUD"],
          ["任务 6 完成", "feat(任务6): 运行时权限与自定义 ContentProvider"],
          ["任务 7 完成", "feat(任务7): 网络请求与 JSON 双解析联调"],
          ["任务 8 完成", "feat(任务8): Service 双启动方式、定位与多媒体"],
          ["任务 9 完成", "feat(任务9): 员工管理 CRUD 前后端全链路联调"],
          ["报告完成", "docs: 提交实验一实验报告与步骤指导"],
      ],
      widths=[4.0, 12.0])

note(doc, "提交前先执行 git status 确认没有把 build/ 之类的产物加进去（.gitignore 已配好）。"
          "推送用 git push -u origin main；如果要求输入密码而失败，"
          "GitHub 现在必须用 Personal Access Token 代替密码，或改用 SSH 方式。")

# ============================================================ 六、常见问题
h1(doc, "六、常见问题速查")

table(doc,
      ["现象", "原因与处理"],
      [
          ["Gradle Sync 卡住或超时",
           "首次要下载依赖。可在 settings.gradle 里把仓库换成阿里云镜像；"
           "确认网络能访问 dl.google.com 与 repo.maven.apache.org。"],
          ["报错 project path contains non-ASCII characters",
           "工程在中文目录。gradle.properties 中加 android.overridePathCheck=true（已加）。"],
          ["中文注释变乱码",
           "compileOptions 中加 encoding 为 UTF-8（已加）。"],
          ["App 请求后端报连接被拒绝",
           "模拟器要用 10.0.2.2 而不是 localhost；确认后端 8080 已监听；"
           "Windows 防火墙放行 java.exe。"],
          ["报 Cleartext HTTP traffic not permitted",
           "Android 9 及以上限制明文 HTTP。Manifest 里加 usesCleartextTraffic 为 true（已加）。"],
          ["后端启动报 Invalid bound statement (not found)",
           "MyBatis 没加载到 mapper XML。application.yml 里必须写 "
           "mapper-locations: classpath*:/mapper/**/*.xml（已加）。"],
          ["读取通讯录是空的",
           "模拟器通讯录默认没数据，先在系统通讯录 App 里加几条。"],
          ["动态注册广播报 leaked IntentReceiver",
           "onDestroy 里漏了 unregisterReceiver，必须成对出现。"],
          ["SQLite 改表结构不生效",
           "onCreate 只在建库时跑一次，要提升 VERSION 触发 onUpgrade，或卸载重装 App。"],
          ["RecyclerView 一片空白",
           "忘了 setLayoutManager 或 setAdapter，或数据源为空。"],
          ["模拟器起不来或黑屏",
           "开启 BIOS 虚拟化与 Windows Hypervisor Platform；"
           "确认 AVD 所在磁盘剩余空间足够，userdata 分区需要几个 GB。"],
      ],
      widths=[5.2, 10.8], font_size=9.5)

# ============================================================ 七、自查
h1(doc, "七、提交前的自查清单")

for item in [
    "9 个任务都能在模拟器上跑出结果，没有崩溃。",
    "每个任务至少 1 张截图，共 33 张，能看清界面或日志内容。",
    "Git 有 9 次以上与任务对应的提交，说明符合 feat(任务N) 的格式。",
    "报告里基础信息（姓名、班级、学号、实验时间、地点）填写完整。",
    "报告的错误描述部分至少有 2 个问题，写全了现象、排查思路、解决方法、整改结果。",
    "AI 使用记录里写清了提示词要点和人工修正的地方，没有整段照抄的嫌疑。",
    "实验总结包含知识点收获、难点、AI 辅助体会与改进方向，18 道思考题都作答。",
    "数据库口令等敏感信息没有硬编码进提交到仓库的代码里（本机实验可接受，但要能解释）。",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(4)
    style_run(p.add_run("□  " + item), size=11.5)

doc.save(OUT)
print("saved:", os.path.abspath(OUT))
