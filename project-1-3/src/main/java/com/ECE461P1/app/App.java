package com.ECE461P1.app;

import com.ECE461P1.app.scores.PackageJson;
import com.ECE461P1.app.scores.Score;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.jcabi.github.Repo;
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
    PackageJson packageJson = new Gson().fromJson(a, PackageJson.class);

//    JSONObject obj = new JSONObject(jsonInput);
    // Gson gson = new Gson();
    // System.out.println(gson.toJson(packageJson).toString());



//    JsonParser parser = new JsonParser();
//    JsonObject object = (JsonObject) parser.parse(a);// response will be the json String
////    YourPojo emp = gson.fromJson(object, YourPojo.class);

    RepoHandler repo = new RepoHandler(packageJson);

    RepoScores rScores = new RepoScores();

    repo.correctnessScore.getCorrectnessScore();
    repo.responseScore.getResponsivenessScore();
    repo.busScore.getBusFactor();
    repo.licenseScore.getLicenseScore();
    repo.rampScore.getRampUpTimeScore();
    repo.depScore.getDependencyRatio();
    repo.calcNetScore();

    rScores.correctnessScore = repo.correctnessScore.getScore();
    rScores.responsivenessScore = repo.responseScore.getScore();
    rScores.busFactor = repo.busScore.getScore();
    rScores.licenseScore = repo.licenseScore.getScore();
    rScores.rampUpTimeScore = repo.rampScore.getScore();
    rScores.dependencyRatio = repo.depScore.getScore();
    rScores.netScore = repo.calcNetScore();

    rScores.url = repo.orgUrl;

    RepoScoresParent rScoresParent = new RepoScoresParent();
    List<RepoScores> rscoreslist = new ArrayList<RepoScores>();
    rscoreslist.add(rScores);
    rScoresParent.Scores = rscoreslist;


    Gson gson = new Gson();


    System.out.println(gson.toJson(rScoresParent));

//
//    repo.calcNetScore();
//    JsonArrayBuilder arrayBuilder = Json.createArrayBuilder();
//    arrayBuilder.add(repo.getJObj());
//    jObj.add("Scores", arrBuilder.build());
//    jWriter.writeObject(jObj.build()); //TODO

  }
}

class RepoScores{
  String url;
  float correctnessScore;
  float responsivenessScore;
  float busFactor;
  float licenseScore;
  float rampUpTimeScore;
  float dependencyRatio;
  float netScore;

  public RepoScores() {
  }

}

class RepoScoresParent{
  List<RepoScores> Scores;
  public RepoScoresParent() {
  }
}

