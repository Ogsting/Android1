package com.example.helloandroid.task3;

/** 任务 3 使用的联系人简单实体，仅本任务演示用。 */
public class Contact {

    private final String name;
    private final String phone;

    public Contact(String name, String phone) {
        this.name = name;
        this.phone = phone;
    }

    public String getName() {
        return name;
    }

    public String getPhone() {
        return phone;
    }
}
