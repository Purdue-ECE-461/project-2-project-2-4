package com.ECE461P1.app;

import com.ECE461P1.app.scores.PackageJson;
import com.google.gson.Gson;
import org.eclipse.jgit.api.Git;

import java.util.ArrayList;
import java.util.List;

public class App
{
  public static Git git;
  //  static final Logger logger = LoggerFactory.getLogger(Score.class);

  public static void main (String[] args) {

    StringBuilder jsonInput = new StringBuilder();
    for (String s : args) {
      jsonInput.append(s);
    }
    JsonHandler jsonHandler = new JsonHandler(jsonInput.toString());

//    System.out.println(jsonInput.toString());
    PackageJson packageJson = jsonHandler.getPackageJson();
//    try {
//      packageJson = new Gson().fromJson(a, PackageJson.class);
//    } catch (Exception e){
////      e.printStackTrace();
//    }

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
    List<RepoScores> rScoresList = new ArrayList<>();
    rScoresList.add(rScores);
    rScoresParent.Scores = rScoresList;

    Gson gson = new Gson();

    String result = gson.toJson(rScoresParent);

    System.out.println(result);

  }
}