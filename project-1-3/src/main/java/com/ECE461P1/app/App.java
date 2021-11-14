package com.ECE461P1.app;

import com.ECE461P1.app.scores.Score;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.eclipse.jgit.api.Git;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.json.Json;
import javax.json.JsonArrayBuilder;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class App
{
  public static Git git;
//  static final Logger logger = LoggerFactory.getLogger(Score.class);

  public static void main (String[] args) {

    StringBuilder jsonInput = new StringBuilder();
    for (String s : args) {
      jsonInput.append(s);
    }
    String a = jsonInput.toString().strip();
//    System.out.println(jsonInput.toString());
    packageJson convertedObject = new Gson().fromJson(a, packageJson.class);

    JSONObject obj = new JSONObject(jsonInput);
    Gson gson = new Gson();
    System.out.println(gson.toJson(convertedObject).toString());



    //    Gson gson = new Gson();
//    JsonParser parser = new JsonParser();
//    JsonObject object = (JsonObject) parser.parse(a);// response will be the json String
////    YourPojo emp = gson.fromJson(object, YourPojo.class);

//    RepoHandler repo = new RepoHandler(obj);


//    repo.correctnessScore.getCorrectnessScore();
//    repo.responseScore.getResponsivenessScore();
//    repo.busScore.getBusFactor();
//    repo.licenseScore.getLicenseScore();
//    repo.rampScore.getRampUpTimeScore();
//    repo.depScore.getDependencyRatio();
//
//    repo.calcNetScore();
//    JsonArrayBuilder arrayBuilder = Json.createArrayBuilder();
//    arrayBuilder.add(repo.getJObj());
//    jObj.add("Scores", arrBuilder.build());
//    jWriter.writeObject(jObj.build()); //TODO

  }
}

class packageJson {
//  public String dependencies;
  public String repository;
  public List<String> dependencies;

  public packageJson() {
  }
}
