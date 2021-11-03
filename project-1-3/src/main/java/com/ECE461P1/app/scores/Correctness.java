package com.ECE461P1.app.scores;

import com.ECE461P1.app.App;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.InvalidRemoteException;
import org.eclipse.jgit.api.errors.JGitInternalException;
import org.eclipse.jgit.api.errors.TransportException;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Correctness extends Score {
  File repoClone;
  Git git = App.git;
  public Correctness(String _owner, String _repo){
    super(_owner, _repo);
    if(new File("./tmpRepo").mkdirs()){
      repoClone = new File("./tmpRepo");
    }
  }
  public void runClone(){
    try{
      cloneRepo();
    }catch(Exception e){
      System.out.println(e);
    }
  }

  public void deleteClone(){
    System.out.println("Deleting repo clone in local directory " + repoClone);
    git.close();
    deleteDirectory(repoClone);
  }

  public File getRepoClone(){
    return repoClone;
  }

  private void cloneRepo() throws InvalidRemoteException, TransportException, GitAPIException, IOException {
    System.out.println("Cloning " + coord + ".git ...");
    try{
      repoClone = new File("./tmpRepo");
      git = Git.cloneRepository()
       .setURI("https://github.com/" + coord + ".git")
       .setDirectory(repoClone)
       .call();
    } catch (JGitInternalException e) {
      System.out.println("Local repo ./tempRepo still exists\nDeleting and trying again...");
      deleteClone();
      cloneRepo();
    } catch (TransportException e2) {
      System.out.println("Failed cloning: Local repo ./tempRepo still exists\nDeleting and trying again...");
      deleteClone();
      cloneRepo();
    }
  }
  private boolean deleteDirectory(File directoryToBeDeleted) {
    File[] allContents = directoryToBeDeleted.listFiles();
    if (allContents != null) {
        for (File file : allContents) {
            deleteDirectory(file);
        }
    }
    Path path = directoryToBeDeleted.toPath();
    boolean deleteSuccess = false;
    try {
      deleteSuccess = Files.deleteIfExists(path);
    } catch (NoSuchFileException x) {
      System.err.format("%s: no such" + " file or directory%n", path.toString());
    } catch (DirectoryNotEmptyException x) {
      System.err.format("%s not empty%n", path.toString());
    } catch (IOException x) {
      // File permission problems are caught here.
      System.err.println(x);
    }
    return deleteSuccess;
  }
  public void getCorrectnessScore(){
    int count = 0;
    System.out.println("Calculating correctness score...");
    runClone();
    try (Stream<Path> walk = Files.walk(Paths.get(repoClone.toString()))) {
      List<String> result = walk.map(x -> x.toString()).filter(f -> (f.contains("test") & (f.endsWith(".js") || f.endsWith(".json")))).collect(Collectors.toList());
      for (String r : result){
        if (!(r==null || r.trim().isEmpty())){count++;}
      }
	  } catch (IOException e) {
      System.out.println(e);
      score = -1.0f;
      return;
	  }
    deleteClone();
    score = ((float) count/150)>=1 ? 1 : ((float) count/150);
   }
}
