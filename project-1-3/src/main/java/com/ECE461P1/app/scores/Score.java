package com.ECE461P1.app.scores;
//import com.ECE461P1.app.Url;
import com.jcabi.github.*;
import java.io.*;
import java.net.*;
import java.util.Base64;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;


//import java.net.http.HttpGet;

import java.net.http.HttpResponse;

public class Score {
  float score = 0.0f;
  String ownerName = "";
  String repoName = "";
  String apiUrl = "";
  String coord = "";
  Github gh = null;
  public Score(String _owner, String _repo){
    ownerName = _owner;
    repoName = _repo;
    coord = ownerName + "/" + repoName;
    apiUrl = "https://api.github.com/repos/" + coord;
  }
  public String getOwnerName(){
    return ownerName;
  }
  public String getRepoName(){
    return repoName;
  }
  public String getApi(){
    return apiUrl;
  }
  public String getCoord(){
    return coord;
  }
  public float getScore(){
    return score;
  }
  public String toString(){
    return Float.toString(score);
  }
  
  public Repo getJgitRepo (String token) {
    if (gh == null) {gh = getGithub(token);}
    return getJgitRepo(gh);
  }
  public Repo getJgitRepo (String token, String property) {
    if (gh == null) {
      if (token == null) {
        gh = getGithub();
      }else{
        gh = getGithub(token);
      }
    }
    String str = coord + "/" + property;
    return gh.repos().get(new Coordinates.Simple(str));
  }
  public Repo getJgitRepo (Github github) {
    return github.repos().get(new Coordinates.Simple(coord));
  }
  public Repo getJgitRepo (Github github, String property) {
    String str = coord + "/" + property;
    return github.repos().get(new Coordinates.Simple(str));
  }
  public Repo getJgitRepo () {
    if (gh == null) {gh = getGithub();}
    return gh.repos().get(new Coordinates.Simple(coord));
  }
  
  public Github getGithub () {
    if (gh == null){gh = new RtGithub(System.getenv("GITHUB_TOKEN"));}
    return gh;
  }
  public Github getGithub (String token) {
    if (gh == null){gh = new RtGithub(token);}
    return gh;
  }
  
  public float checkExistance(){
    try { //check if repo exists
      URL conUrl = new URL(apiUrl + "/readme");
      int respon = httpreq(conUrl);
      if (respon != 200){score = -1.0f;}
    } catch (Exception e){
      System.out.println("Exception in Score.checkExistance: " + e);
      score = -1.0f;
    }
    return score;
  }
  
  public int httpreq(URL conUrl) throws MalformedURLException, IOException{
    System.out.println("URL from conURL: " + conUrl.toString());

//    HttpURLConnection conn = (HttpURLConnection) conUrl.openConnection();
//    System.out.println("URL from conURL: " + conn.getHeaderField(0));
//    System.out.println("Token: " + System.getenv("GITHUB_TOKEN"));
    HttpClient client = HttpClient.newHttpClient();
//
    HttpRequest request = HttpRequest.newBuilder()
            .header("Authorization", "Bearer " + System.getenv("GITHUB_TOKEN"))
            .uri(URI.create(conUrl.toString()))
            .build();
    HttpResponse<String> response;
    try {
      response = client.send(request, HttpResponse.BodyHandlers.ofString());
//              .thenApply(HttpResponse::body)
//              .thenAccept(System.out::println)
//              .join();
      // System.out.println("HttpClient response code:" + response.statusCode());
      // System.out.println(response.body());
      // System.out.println(response.headers().allValues("x-ratelimit-remaining"));

    } catch (Exception e) {
      System.out.println("HTTPClient client.send exception: " + e);
      return 0;
    }

//    HttpGet request = new HttpGet(url);
//    HttpRequest.newBuilder().header("Authorization","Bearer <myToken>")
//            .uri(URI.create("https://api.github.com/repos/:owner/:repo/commits"))
//            .build();

    int respon = 0;

    try {
      respon = response.statusCode();

      if (respon == 200) {
        System.out.println("RESPONSE = 200");
//      System.out.println("Response Code " + String.valueOf(respon) + " OK");
      } else if (respon == 301) {
        System.out.println(response.headers().allValues("Location"));
        conUrl = new URL(response.headers().allValues("Location").toString());
        respon = httpreq(conUrl);
      } else if (respon == 403) {
        System.out.println("url: " + conUrl + "\nUser has hit hourly http request limit. Please wait an hour and try again.");
      } else {
        System.out.print("In Else block: ");
        String str = "\nurl: " + conUrl + "\nResponse Code not OK: " + String.valueOf(respon);
        throw new MalformedURLException(str);
      }
    } catch (Exception e) {
      System.out.println("Exception in httpreq: ");
      e.printStackTrace();
      throw e;
    }
    return respon;
  }
}

