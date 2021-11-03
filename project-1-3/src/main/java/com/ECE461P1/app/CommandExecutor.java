package com.ECE461P1.app;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Map;

//code refers to https://stackoverflow.com/questions/40503074/how-to-run-npm-command-in-java-using-process-builder
//To see available NPM commands, go to https://docs.npmjs.com/cli/v7/commands
public class CommandExecutor {
  public String exceuteCommand(String commandString,String directoryToExecuteCommand) throws IOException{
      ProcessBuilder processBuilder = new ProcessBuilder("bash", "-c",commandString);
      Map<String, String> env = processBuilder.environment();
      processBuilder.directory(new File(directoryToExecuteCommand));
      //String envPath="/home/"+System.getenv("USER")+"/.nvm/versions/node/v10.15.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin";
      //env.put("PATH",envPath);
      Process resultExecution=processBuilder.start();
      BufferedReader br=new BufferedReader(new InputStreamReader(resultExecution.getInputStream()));
      StringBuffer sb=new StringBuffer();
      String line;
      while((line=br.readLine())!=null){
        sb.append(line);
      }
      br.close();
      return sb.toString();
  }
  
  public static void main(String args[]) {
    CommandExecutor commandExecutor=new CommandExecutor();
    try{
      String test = commandExecutor.exceuteCommand("npm view " + args[0] + " repository.url", "./node-v16.13.0-darwin-x64/bin/");
      System.out.println("TEST: " + test);
    } catch (IOException e) {
      System.out.println("npm processbuilder could not find directory " + "./node-v14.18.0-linux-x64/bin/");
    }
  }
}