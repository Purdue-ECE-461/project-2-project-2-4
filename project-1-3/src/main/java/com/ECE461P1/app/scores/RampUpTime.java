package com.ECE461P1.app.scores;

import java.io.*;
import java.net.*;
import com.jcabi.github.*;
import javax.json.*;

public class RampUpTime extends Score {
  private float scoreScale = 0.25f;
  private float forkScale = 0.0001f;

  public RampUpTime (String _owner, String _repo){
    super(_owner, _repo);
  }

  private float readmeHelper () {
    Repo readmeRepo = getJgitRepo(gh, "readme");

    JsonObject info = null;
    try {
      info = readmeRepo.json();
      return (float) info.getInt("size");
    } catch (Exception e) {
      System.out.println(e);
      return 0.0f;
    }
  }

  private float fileCountHelper () {
    Repo fileCountRepo = getJgitRepo(gh, "git/trees/master");

    JsonObject info = null;
    float fileCount = 0.0f;

    try {
      info = fileCountRepo.json();
    } catch (IOException e) {
      System.out.println(e);
    }

    JsonArray tree = info.getJsonArray("tree");
    String sha = info.getString("sha");
    fileCount += fileCountHelperRecur(gh, tree, sha);

    return fileCount;
  }

  private float fileCountHelperRecur (Github gh, JsonArray tree, String sha) {
    float fileCount = 0.0f;
    JsonObject node;
    String subTreeCoord;
    Repo subTreeRepo;
    JsonObject subTreeInfo = null;
    String subTreeSha;
    JsonArray subTree;

    for (int i = 0; i < tree.size(); i++) {
      node = tree.getJsonObject(i);

      if (!node.getString("type").equals("tree")) {
        fileCount++;
      } else {
        subTreeCoord = "git/trees/" + node.getString("sha");
        subTreeRepo = getJgitRepo(gh, subTreeCoord);

        try {
          subTreeInfo = subTreeRepo.json();
        } catch (IOException e) {
          System.out.println(e);
        }

        subTreeSha = node.getString("sha");
        subTree = subTreeInfo.getJsonArray("tree");

        fileCount += fileCountHelperRecur(gh, subTree, subTreeSha);
      }
    }

    return fileCount;
  }

  private float forkCountHelper () {
    Repo fileCountRepo = getJgitRepo();

    JsonObject info = null;

    try {
      info = fileCountRepo.json();
    } catch (IOException e) {
      System.out.println(e);
    }

    return (float) info.getInt("forks");
  }

  public float getRampUpTimeScore () {
    System.out.println("Calculating ramp up time score...");
    Github gh = getGithub();
    
    float rampUpTimeScore = 0.0f;
    float readmeSize = readmeHelper();
    //System.out.println(readmeSize);
    float fileCount = fileCountHelper();
    //System.out.println(fileCount);
    float forkCount = forkCountHelper();
    //System.out.println(forkCount);

    rampUpTimeScore = scoreScale * (readmeSize / fileCount + forkScale * forkCount);

    if (rampUpTimeScore > 1.0f) {
      rampUpTimeScore = 1.0f;
    }

    //System.out.println(rampUpTimeScore);
    score = rampUpTimeScore;
    return score;
  }

  public static void main (String[] args) {
//    RampUpTime test = new RampUpTime("walletconnect", "walletconnect-example-dapp");
//    RampUpTime test = new RampUpTime("mochajs", "mocha");
//    RampUpTime test = new RampUpTime("edapaker", "Fraction-Approximation");
    RampUpTime test = new RampUpTime("Tencent", "phxpaxos");
//    RampUpTime test = new RampUpTime("okmr-d", "DOFavoriteButton");
    System.out.println(test.getRampUpTimeScore());
  }
}