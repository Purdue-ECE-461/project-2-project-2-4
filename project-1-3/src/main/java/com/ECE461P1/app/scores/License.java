package com.ECE461P1.app.scores;

import com.jcabi.github.*;

import javax.json.JsonObject;
import java.io.IOException;

public class License extends Score {
  private String[] validLicenses = {"\"lgpl-2.1\"", "\"lgpl-3.0\"", "\"gpl-2.0\"", "\"gpl-3.0\"", "\"mpl-2.0\"", "\"apache-2.0\"", "\"bsl-1.0\"", "\"mit\""};

  public License (String _owner, String _repo) {
    super(_owner, _repo);
  }

  public float getLicenseScore () {
//    System.out.println("Calculating license score...");
    
    Repo licenseRepo = getJgitRepo();
    JsonObject info = null;
    JsonObject license = null;

    try {
      info = licenseRepo.json();
    } catch (IOException e) {
//      System.out.println(e);
    }

    if (info.isNull("license")) {
      score = (float) 0;
      return score;
    } else {
      license = info.getJsonObject("license");
    }

    for (String validLicense : validLicenses) {
      if (validLicense.equals(license.getJsonString("key").toString())) {
        //System.out.println("Success");
        score = (float) 1;
        return score;
      }
    }
    
    score = (float) 0;
    return score;
  }

  public static void main (String[] args) {
    License test = new License("jonschlinkert", "even");
    test.getLicenseScore();
  }
}