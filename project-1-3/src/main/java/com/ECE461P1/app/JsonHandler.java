package com.ECE461P1.app;

import com.ECE461P1.app.scores.PackageJson;
import com.google.gson.Gson;

public class JsonHandler {

    PackageJson packageJson;

    public PackageJson getPackageJson() {
        return packageJson;
    }
    public JsonHandler(String jsonInput) {
        try {
            packageJson = new Gson().fromJson(jsonInput.strip(), PackageJson.class);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
