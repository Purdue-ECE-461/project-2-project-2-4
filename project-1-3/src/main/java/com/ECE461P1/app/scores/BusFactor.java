package com.ECE461P1.app.scores;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class BusFactor extends Score {
  static int i = 0;
  public BusFactor(String _owner, String _repo){
    super(_owner, _repo);
  }

  public HttpURLConnection makeHttpConnection() throws java.io.IOException{
      URL contributorsUrl = new URL(apiUrl + "/contributors");
      int respon = httpreq(contributorsUrl);
      HttpURLConnection conn = (HttpURLConnection) contributorsUrl.openConnection();
      conn.setRequestMethod("GET");
      conn.setRequestProperty("Authorization", "token " + System.getenv("GITHUB_TOKEN"));
      if (respon == 200) {
        return conn;
      } else {
        throw new java.io.IOException();
      }
  }

  public void getBusFactor() {
    System.out.println("Calculating bus factor score...");
    try {
      //jcabi does not implement jsonArrays, using HttpURLConnection directly instead
//      URL contributorsUrl = new URL(apiUrl + "/contributors");
//      int respon = httpreq(contributorsUrl);
//      HttpURLConnection conn = (HttpURLConnection) contributorsUrl.openConnection();
//      conn.setRequestMethod("GET");
//      conn.setRequestProperty("Authorization", "token " + System.getenv("GITHUB_TOKEN"));
        HttpURLConnection conn = makeHttpConnection();
//      if (respon == 200) {
        BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String tempLine = rd.readLine();
        String[] tempLineArr = tempLine.split("\"login\":", -1);
        i = (tempLineArr.length) - 1; //max from api is 30
        rd.close();
//      }
    } catch (Exception e){
      System.out.println("Exception in getBusFactor: " + e);
    }

    score = ((i >= 6) ? 1 : ((float) i / 6));
    i = 0; // reset static i for next url
  }
}

