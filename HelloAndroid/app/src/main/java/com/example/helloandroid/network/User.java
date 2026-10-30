package com.example.helloandroid.network;

/** 任务 7：演示接口返回的用户实体，字段名必须与后端 JSON 一致。 */
public class User {

    private long id;
    private String username;
    private String nickname;
    private int age;
    private String email;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return nickname + "（" + username + "，" + age + "岁，" + email + "）";
    }
}
