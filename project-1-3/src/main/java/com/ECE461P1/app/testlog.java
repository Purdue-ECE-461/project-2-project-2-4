package com.ECE461P1.app;

import org.jsoup.*;
import org.jsoup.nodes.*;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Arrays;
import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class testlog {
  static int numTests = 0;
  static int passedTests = 0;
  static int lineCoverage = -1;
  public static void main(String[] args) {
    PrintStream console = System.out;
    try {
      File logFile = new File(System.getenv("LOG_FILE"));
      PrintStream o = new PrintStream(logFile);
      System.setOut(o);
    } catch (Exception e){
      System.out.println("Testing failed: unable to redirect stdout");
    }
    //parse coverage report
    try {
      File input = new File("./jacoco/index.html");
      Document doc = Jsoup.parse(input, "UTF-8");
      String tdLine = doc.select("td.ctr2:contains(%)").first().toString();
      Pattern p = Pattern.compile("<td class=.ctr2.>(\\d+)%<\\/td>");
      Matcher m = p.matcher(tdLine);
      m.find();
      lineCoverage = Integer.parseInt(m.group(1));
    } catch (IOException e){
    } catch (Exception e2){
      System.out.println(e2);
    }
    testing(); //get passedTests/numTests
    System.out.println("\n" + passedTests + "/" + numTests + " test cases passed. " + lineCoverage + "% line coverage achieved.");
    System.setOut(console);
  }
  
  public static void testing() {
    System.out.println("\nTESTING:");
    System.out.println("\ntesting https connection...");
    numTests++;
    int response = 0;
    try {
      URL conUrl = new URL("http://api.github.com/repos/octocat/Hello-World");
      response = httpreq(conUrl);
    }catch(Exception e){
      System.out.println(e);
    }
    if (response == 200){
      passedTests++;
      System.out.println("test http connect succeeded");
    } else{
      System.out.println("test http connect failed");
    }

    System.out.println("\ntesting parseUrl for github.com input...");
    numTests++;
    Url urlgit = new Url("https://www.github.com/octocat/Hello-World");
    if (urlgit.getAPIUrl() != "") {
      passedTests++;
      System.out.println("test parseUrl succeeded");
    } else {
      System.out.println("test parseUrl failed");
    }

    System.out.println("\ntesting parseUrl for npmjs.com input...");
    numTests++;
    Url urlnpm = new Url("https://www.npmjs.com/package/native-hello-world");
    if (urlnpm.getAPIUrl() != "") {
      passedTests++;
      System.out.println("test parseUrl npm succeeded");
    } else {
      System.out.println("test parseUrl npm failed");
    }

    System.out.println("\ntesting repository cloning...");
    boolean cloneTest;
    try{cloneTest = testCorrectness(urlgit);}
    catch(NullPointerException e){cloneTest = false;}
    if(!cloneTest){
      try{cloneTest = testCorrectness(urlnpm);}
      catch(NullPointerException e){cloneTest = false;}
    }

    //add other tests here, make function below if needed (see testCorrectness)

    //MUST BE LAST TEST, required for finding code coverage
    System.out.println("\ntesting full run with test urls for code coverage ...");
    Url[] urls = App.parseURLS(new File("UrlTest.txt"));
    for (Url url : urls){
      if(url.correctnessScore == null){continue;}//com.ECE461P1.app.scores where not initialized because http request limit has been reached
      
      numTests++;
      System.out.println("\nTesting correctness on url: " + url.getOrginalUrl());
      url.correctnessScore.getCorrectnessScore();
      if (url.correctnessScore.getScore() != -1.0f) {passedTests++;
      System.out.println("Testing correctness succeeded");}
      else{System.out.println("Testing correctness failed");}
      
      numTests++;
      System.out.println("\nTesting responsiveness on url: " + url.getOrginalUrl());
      url.responseScore.getResponsivenessScore();
      if (url.responseScore.getScore() != -1.0f) {passedTests++;
      System.out.println("Testing responsiveness succeeded");}
      else{System.out.println("Testing responsiveness failed");}
      
      numTests++;
      System.out.println("\nTesting bus factor on url: " + url.getOrginalUrl());
      url.busScore.getBusFactor();
      if (url.busScore.getScore() != -1.0f) {passedTests++;
      System.out.println("Testing bus factor succeeded");}
      else{System.out.println("Testing bus factor failed");}
      
      numTests++;
      System.out.println("\nTesting license on url: " + url.getOrginalUrl());
      url.licenseScore.getLicenseScore();
      if (url.licenseScore.getScore() != -1.0f) {passedTests++;
      System.out.println("Testing license succeeded");}
      else{System.out.println("Testing license failed");}
      
      numTests++;
      System.out.println("\nTesting ramp-up time on url: " + url.getOrginalUrl());
      url.rampScore.getRampUpTimeScore();
      if (url.rampScore.getScore() != -1.0f) {passedTests++;
      System.out.println("Testing ramp-up time succeeded");}
      else{System.out.println("Testing ramp-up time failed");}
    }
    
    System.out.println("\nURL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE");
    Arrays.sort(urls, Comparator.comparingInt(url ->
      (url!=null & url.correctnessScore!=null) ? (int) url.calcNetScore() : 0
    ));
    for (Url url : urls) {System.out.println(url);}
  }

  public static int httpreq(URL conUrl) throws MalformedURLException, IOException{
    System.out.println("Entered httpreq; conURL = " + conUrl);
    HttpURLConnection conn = (HttpURLConnection) conUrl.openConnection();
    conn.setRequestMethod("GET");
    conn.setRequestProperty("Authorization", "token " + System.getenv("GITHUB_TOKEN"));
    System.out.println("TOKEN = " + System.getenv("GITHUB_TOKEN"));

//    HttpClient client = HttpClient.newHttpClient();
//
//    HttpRequest request = HttpRequest.newBuilder()
//            .uri(URI.create("https://api.github.com/repos/:owner/:repo/commits"))
//            .header("Authorization", "your-token")
//            .build();
    int respon = 0;
    try{
      respon = conn.getResponseCode();
    }catch(IOException e2){
      System.out.println(e2);
    }
    if (respon == 200) {
      System.out.println("Response Code " + respon + " OK");
    } else if (respon == 301){
      conUrl = new URL(conn.getHeaderField("Location"));
      respon = httpreq(conUrl);
    } else if (respon == 403){
      System.out.println("url: " + conUrl + "\nUser has hit hourly http request limit. Please wait an hour and try again");
    } else {System.out.println("url: " + conUrl + "\nResponse Code not OK: " + respon);}
    return respon;
  }

  public static boolean testCorrectness(Url url){
    numTests++;
    url.correctnessScore.runClone();
    if ((url.correctnessScore.getRepoClone()).exists()) {
      passedTests++;
      System.out.println("test testCorrectness.runClone succeeded");
    } else {
      System.out.println("test testCorrectness.runClone failed");
      return false;
    }
    
    numTests++;
    url.correctnessScore.deleteClone();
    if (!((url.correctnessScore.getRepoClone()).exists())) {
      passedTests++;
      System.out.println("test testCorrectness.deleteClone succeeded");
    } else {
      System.out.println("test testCorrectness.deleteClone failed");
      return false;
    }
    
    
      numTests++;
      url.correctnessScore.runClone();
      url.correctnessScore.runClone();
      url.correctnessScore.deleteClone();
      if (!((url.correctnessScore.getRepoClone()).exists())) {
        passedTests++;
        System.out.println("test testCorrectness.deleteCloneErrorHandle succeeded");
        return true;
      } else {
        System.out.println("test testCorrectness.deleteCloneErrorHandle failed");
        return false;
      }
  }
}
