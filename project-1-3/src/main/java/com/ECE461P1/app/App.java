package com.ECE461P1.app;
import java.io.*;
import java.util.*;
import org.eclipse.jgit.api.Git;

public class App
{
  public static Git git;
  public static void main (String[] args) {
    Url[] urls = parseURLS(new File(args[0]));
    for (Url url : urls){
      if(url.correctnessScore == null){continue;}//scores where not initalized because http request limit has been reached
      url.correctnessScore.getCorrectnessScore();
      url.responseScore.getResponsivenessScore();
      url.busScore.getBusFactor();
      url.licenseScore.getLicenseScore();
      url.rampScore.getRampUpTimeScore();
    }
    
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
