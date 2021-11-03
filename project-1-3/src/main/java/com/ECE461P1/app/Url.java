package com.ECE461P1.app;

import com.ECE461P1.app.scores.*;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

public class Url {
  private String orgUrl = "";
  private String orgDomain = "";
  String ownerName = "";
  String repoName = "";
  String apiUrl = "";
  float netScore = 0.0f;
  Score s = new Score(ownerName,repoName);
  BusFactor busScore;
  Correctness correctnessScore;
  RampUpTime rampScore;
  License licenseScore;
  Responsiveness responseScore;
  
  public Url(String _url){
    orgUrl = _url;

    boolean parseCheck = parseUrl(orgUrl);
    if (!parseCheck) {
      System.out.println("There was an error parsing the url: " + orgUrl);
      return;
    }


    s = new Score(ownerName,repoName);
    apiUrl = s.getApi();
    float score = s.checkExistance();
    if(score == -1.0f){return;}

    busScore = new BusFactor(ownerName, repoName);
    correctnessScore = new Correctness(ownerName, repoName);
    licenseScore = new License(ownerName, repoName);
    rampScore = new RampUpTime(ownerName, repoName);
    responseScore = new Responsiveness(ownerName, repoName);
  }

  public String getOrginalUrl(){
    return orgUrl;
  }
  public String getOrginalDomain(){
    return orgDomain;
  }
  public String getAPIUrl(){
    return apiUrl;
  }
  public float calcNetScore(){
    netScore = (float) 0.4 * correctnessScore.getScore();
    netScore += (float) 0.3 * rampScore.getScore();
    netScore += (float) 0.2 * responseScore.getScore();
    netScore += (float) 0.1 * busScore.getScore();
    netScore *= licenseScore.getScore();
    return netScore;
  }
  public String toString(){
    if(correctnessScore == null){//com.ECE461P1.app.scores where not initalized because http request limit has been reached
      String str = "" + orgUrl + " 0.0 0.0 0.0 0.0 0.0 0.0";
      return str;
    }
    String str = "" + orgUrl + " " + netScore + " " + rampScore + " " + correctnessScore + " " + busScore + " " + responseScore + " " + licenseScore;
    return str;
  }

  private boolean parseUrl(String url){
    Pattern p = Pattern.compile("(http|https):\\/\\/(www.)?(.*).com\\/(.*)\\/(.*)$");
    try {
      Matcher m = p.matcher(url);
      m.find();
      orgDomain = m.group(3);
//      System.out.println(orgDomain);
      if (orgDomain.equals("npmjs")) {
        String packageName = m.group(5);
        //NPM API get repo url
        CommandExecutor commandExecutor=new CommandExecutor();
        String giturl = "";
        try{
          giturl = commandExecutor.exceuteCommand("npm view " + packageName + " repository.url", "./usr/local/bin/");
        } catch(IOException e){
          System.out.println("1st NPM COMMAND FAILED");
          try{
            giturl = commandExecutor.exceuteCommand("npm view " + packageName + " repository.url", "./");
          } catch(IOException e2){
            System.out.println("2nd NPM COMMAND FAILED");

            System.out.println("npm command executor could not find npm");
            return false;
          }
        }

        Pattern gitp = Pattern.compile("git\\+(ssh|https)?:\\/\\/(git@)?github\\.com\\/(.*)\\/(.*)\\.git");
        try {
          System.out.println(giturl);
          Matcher repo = gitp.matcher(giturl);

          repo.find();
          ownerName = repo.group(3);
          System.out.println(ownerName);
          repoName = repo.group(4);
        }
        catch(PatternSyntaxException e){
          System.out.println("UrlParser NPM Regex failed. URL: " + giturl);
          return false;
        }
      }
      else if (orgDomain.equals("github")) {
        ownerName = m.group(4);
        repoName = m.group(5);
      }
      else {
        System.out.println("Domain " + orgDomain + ".com not supported.");
        return false;
      }
      return true;
    }
    catch(Exception e){
      e.printStackTrace();
      System.out.println("UrlParser Regex failed. URL: " + url);
      return false;
    }
  }
}
