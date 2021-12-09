package com.ECE461P1.app;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
import org.junit.jupiter.params.provider.ValueSource;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.Scanner;

import static org.junit.jupiter.api.Assertions.*;

class JsonHandlerTest {
    @ParameterizedTest
    @CsvFileSource(resources = "/initJsonHandler.csv")
    void jsonHandlerInit(String input) {
//        String content = "";
//        try {
//            content = new Scanner(new File("package-test-files/" + input)).useDelimiter("\\Z").next();
//        } catch (FileNotFoundException e) {
//            e.printStackTrace();
//        }
//        System.out.println(content);
//        JsonHandler j = new JsonHandler(content);
//        String repository = j.getPackageJson().repository;
//        Collection<String> dependencies = j.getPackageJson().dependencies;

    }

}