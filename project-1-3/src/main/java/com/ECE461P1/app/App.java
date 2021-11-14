package com.ECE461P1.app;

import com.ECE461P1.app.scores.Score;
import org.eclipse.jgit.api.Git;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

public class App
{
  public static Git git;
  static final Logger logger = LoggerFactory.getLogger(Score.class);

  public static void main (String[] args) {
    Url[] urls = parseURLS(new File(args[0]));
    for (Url url : urls){
      if(url.correctnessScore == null){continue;}//com.ECE461P1.app.scores where not initalized because http request limit has been reached
      url.correctnessScore.getCorrectnessScore();
      url.responseScore.getResponsivenessScore();
      url.busScore.getBusFactor();
      url.licenseScore.getLicenseScore();
      url.rampScore.getRampUpTimeScore();
    }
    logger.warn("starting");
    
    System.out.println("\nURL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE");
    Arrays.sort(urls, Comparator.comparingInt(url ->
      (url!=null && url.correctnessScore!=null) ? (int) url.calcNetScore() : 0
    ));
    for (Url url : urls) {System.out.println(url);}
  }
  public static Url[] parseURLS(File urlFile) {
    ArrayList<Url> urls = new ArrayList<Url>();
    Scanner sc;
    try{
      sc = new Scanner(urlFile);
      while (sc.hasNextLine()){
        urls.add(new Url(sc.nextLine()));
      }
    }catch(FileNotFoundException e){
      System.out.println("File not Found: " + urlFile);
      return null;
    }
    sc.close();
    Url[] arr = urls.toArray(new Url[urls.size()]);
    return arr;
  }
}
