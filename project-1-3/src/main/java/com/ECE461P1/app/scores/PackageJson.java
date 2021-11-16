package com.ECE461P1.app.scores;

import java.util.Collection;
import java.util.List;

public class PackageJson {

    //  public String dependencies;
    public String repository;
    public Collection<String> dependencies;

    public PackageJson() {
    }

    public String getRepoPath() {
        return repository;
    }
}

