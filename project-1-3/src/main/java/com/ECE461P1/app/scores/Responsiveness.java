package com.ECE461P1.app.scores;

import com.jcabi.github.*;

import javax.json.JsonObject;
import java.io.IOException;
import java.util.EnumMap;

public class Responsiveness extends Score {
  public Responsiveness (String _owner, String _repo){
    super(_owner, _repo);
  }

  private float openIssueCountHelper (Repo issueCountRepo) {
    JsonObject info = null;
    float issueCount;

    try {
      info = issueCountRepo.json();
    } catch (IOException e) {
      System.out.println(e);
    }

    issueCount = (float) info.getInt("open_issues_count");

    return issueCount;
  }

  private float closedIssueCountHelper (Repo issueCountRepo) {
    EnumMap<Issues.Qualifier, String> qualifiers = new EnumMap<Issues.Qualifier, String>(Issues.Qualifier.class);
    qualifiers.put(Issues.Qualifier.STATE, "closed");

    Iterable<Issue> info = null;
    int issueCount = 0;

    try {
      info = issueCountRepo.issues().search(Issues.Sort.UPDATED, Search.Order.DESC, qualifiers);
    } catch (IOException e) {
      System.out.println(e);
    }

    for (Issue test : info) {
      issueCount++;
    }

    return (float) issueCount;
  }

  private float lastClosedIssueHelper (Repo issueCountRepo) {
    EnumMap<Issues.Qualifier, String> qualifiers = new EnumMap<Issues.Qualifier, String>(Issues.Qualifier.class);
    qualifiers.put(Issues.Qualifier.STATE, "closed");

    Iterable<Issue> info = null;
    String createdDate = "";
    String closedDate = "";
    int createdDay;
    int closedDay;

    try {
      info = issueCountRepo.issues().search(Issues.Sort.UPDATED, Search.Order.DESC, qualifiers);
    } catch (IOException e) {
      System.out.println(e);
    }

    try {
      createdDate = info.iterator().next().json().getString("created_at");
      closedDate = info.iterator().next().json().getString("closed_at");
    } catch (IOException e) {
      System.out.println(e);
    }

    createdDay = Integer.parseInt(createdDate.substring(5, 7));
    closedDay = Integer.parseInt(closedDate.substring(5, 7));

    return (float) closedDay - createdDay;
  }

  public float getResponsivenessScore () {
    System.out.println("Calculating responsiveness score...");
    Github gh = getGithub();
    Repo issueCountRepo = getJgitRepo();
    
    float responsivenessScore = 0.0f;
    float openIssueCount = openIssueCountHelper(issueCountRepo);
    //System.out.println(openIssueCount);
    float closedIssueCount = closedIssueCountHelper(issueCountRepo);
    //System.out.println(closedIssueCount);
    float lastClosedIssue = lastClosedIssueHelper(issueCountRepo);
    //System.out.println(lastClosedIssue);

    responsivenessScore = (closedIssueCount / (closedIssueCount + openIssueCount));
    responsivenessScore += (lastClosedIssue > 90 ? 0 : 90 - lastClosedIssue) / 90;
    responsivenessScore /= 2;
    
    score = responsivenessScore;
    return responsivenessScore;
  }

  public static void main (String[] args) {
    //Responsiveness test = new Responsiveness("mochajs", "mocha");
    //Responsiveness test = new Responsiveness("walletconnect", "walletconnect-example-dapp");
    //Responsiveness test = new Responsiveness("Tencent", "phxpaxos");
    Responsiveness test = new Responsiveness("okmr-d", "DOFavoriteButton");
    System.out.println(test.getResponsivenessScore());
  }
}