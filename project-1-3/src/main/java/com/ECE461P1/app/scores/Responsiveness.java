package com.ECE461P1.app.scores;

import com.jcabi.github.*;
import org.json.*;

import javax.json.JsonObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
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
//    Repo issueCountRepo = gh.repos()
//            .get("https://api.github.com/search/issues?q=repo:" + ownerName
//                    + "/" + repoName + "+type:issue+state:closed");
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

  public HttpURLConnection makeRespUrlConn(String path){
    try {

       HttpURLConnection conn =  makeHttpConnection(path);
//      conn.setRequestProperty("User-Agent", "Mozilla/5.0");
      int responseCode = conn.getResponseCode();
//      System.out.println("\nSending 'GET' request to URL : " + url);
      System.out.println("Response Code : " + responseCode);
      BufferedReader in = new BufferedReader(
              new InputStreamReader(conn.getInputStream()));
      String inputLine;
      StringBuffer response = new StringBuffer();
      while ((inputLine = in.readLine()) != null) {
        response.append(inputLine);
      }
      in.close();
      //print in String
      System.out.println(response.toString());
      JSONArray myResponse = new JSONArray(response.toString());
      myResponse.getString(1);
//      System.out.println(count);

    } catch (IOException e) {
      e.printStackTrace();
    }
    return null;
  }

  public static void main (String[] args) {
    //Responsiveness test = new Responsiveness("mochajs", "mocha");
    //Responsiveness test = new Responsiveness("walletconnect", "walletconnect-example-dapp");
    //Responsiveness test = new Responsiveness("Tencent", "phxpaxos");
    Responsiveness test = new Responsiveness("okmr-d", "DOFavoriteButton");
    System.out.println(test.getResponsivenessScore());
  }
}