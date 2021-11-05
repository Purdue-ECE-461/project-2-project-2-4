package com.ECE461P1.app.scores;
import com.ECE461P1.app.scores.Score;
import org.apache.commons.io.IOUtils;

import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;
//import java.io.InputStream;

public class DependencyRatio extends Score{

    public DependencyRatio(String _owner, String _repo) {
        super(_owner, _repo);
    }

//    public HttpURLConnection makeHttpConnection() throws java.io.IOException{
//        URL gQLUrl = new URL("https://api.github.com/graphql");
//        int respon = httpreq(gQLUrl);
//        HttpURLConnection conn = (HttpURLConnection) gQLUrl.openConnection();
//        conn.setRequestMethod("POST");
//        conn.setDoOutput(true);
//        conn.setDoInput(true);
//        conn.setRequestProperty("Authorization", "token " + System.getenv("GITHUB_TOKEN"));
//        conn.setRequestProperty("Accept", "application/vnd.github.hawkgirl-preview+json");
//        conn.setRequestProperty("Content-Type", "application/json");
////        {repository(owner: "node-facebook", name: "facebook-node-sdk") {description}}
//
//        DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
////        wr.writeBytes("{\"query\":\"query{search(type:USER query:\"location:lagos language:java\"){userCount}}}");
//        wr.writeBytes("{\"query\":{\nrepository(owner: \"node-facebook\", name: \"facebook-node-sdk\"){\ndescription\n}\n}");
//
//
//        wr.flush();
//        wr.close();
//
//        String jsonResponse = "";
//        java.io.InputStream inputStream = null;
//
//        int rc = conn.getResponseCode();
//
//        inputStream = conn.getInputStream();

//        StringWriter writer = new StringWriter();
//        IOUtils.copy(inputStream, writer);
//        String theString = writer.toString();
//        jsonResponse = readFromStream(inputStream);


//        if (respon == 200) {
//            return conn;
//        } else {
//            throw new java.io.IOException();
//        }
//    }

    public void getDependencyRatio() {
        try {
//            HttpURLConnection conn = makeHttpConnection();
            score = (float) 1;
        } catch (Exception e) {
            score = (float) 0;
        }

    }

}
