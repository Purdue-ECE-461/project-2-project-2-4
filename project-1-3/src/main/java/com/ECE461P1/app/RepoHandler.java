package com.ECE461P1.app;

import com.ECE461P1.app.scores.*;
import org.json.JSONObject;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;

public class RepoHandler {
  String orgUrl = "";
  String orgDomain = "";
  public String ownerName = "";
  public String repoName = "";
  String apiUrl = "";
  float netScore = 0.0f;
  Score s = new Score(ownerName, repoName);
  BusFactor busScore;
  Correctness correctnessScore;
  RampUpTime rampScore;
  License licenseScore;
  Responsiveness responseScore;
  JsonObjectBuilder jObj;
  DependencyRatio depScore;
  JsonReadHandler jReadHandler;
  PackageJson repo;


  public RepoHandler(PackageJson _repo) {
//    jReadHandler = new JsonReadHandler(_repo);
    repo = _repo;
    orgUrl = repo.getRepoPath();
    String[] strlist = orgUrl.split("\\/");
    ownerName = strlist[0];
    repoName  = strlist[1];
//      orgUrl = _url;

//      boolean parseCheck = parseUrl(orgUrl);
//      if (!parseCheck) {
//        System.out.println("There was an error parsing the url: " + orgUrl);
//        return;
//     }

//    jObj = Json.createObjectBuilder();
    s = new Score(ownerName, repoName);
    apiUrl = s.getApi();
    float score = s.checkExistence();
    if (score == -1.0f) {
      return;
    }

    busScore = new BusFactor(ownerName, repoName);
    correctnessScore = new Correctness(ownerName, repoName);
    licenseScore = new License(ownerName, repoName);
    rampScore = new RampUpTime(ownerName, repoName);
    responseScore = new Responsiveness(ownerName, repoName);
    depScore = new DependencyRatio(repo.dependencies);
//    float depScoreNum = depScore.getScore();

//    System.out.println("Dependency score: " + score);
  }

  public float getBusScore() {
    busScore.getBusFactor();
    return busScore.getScore();
  }

  public String getOrginalUrl() {
    return orgUrl;
  }

  public String getOrginalDomain() {
    return orgDomain;
  }

  public String getAPIUrl() {
    return apiUrl;
  }

  public JsonObject getJObj() {
    return jObj.build();
  }

  public float calcNetScore() {
    netScore = (float) 0.3 * correctnessScore.getScore();
//    System.out.println(netScore);
//    jObj.add("correctnessScore", correctnessScore.getScore());

    netScore += (float) 0.25 * rampScore.getScore();
//    System.out.println(netScore);

//    jObj.add("rampScore", rampScore.getScore());

    netScore += (float) 0.2 * responseScore.getScore();
//    System.out.println(netScore);

    netScore += (float) 0.15 * depScore.getScore();
//    System.out.println(netScore);

    netScore += (float) 0.1 * busScore.getScore();
//    System.out.println(netScore);

    netScore *= licenseScore.getScore();
//    System.out.println(netScore);

//    jObj.addToArray();
//    jObj.write();

    return netScore;
  }


  public String toString() {
    if (correctnessScore == null) {//com.ECE461P1.app.scores where not initalized because http request limit has been reached
      String str = "" + orgUrl + " 0.0 0.0 0.0 0.0 0.0 0.0";
      return str;
    }
    String str = "" + orgUrl + " " + netScore + " " + rampScore + " " + correctnessScore + " " + busScore + " " + responseScore + " " + licenseScore;
    return str;
  }
}
