package com.ECE461P1.app.scores;
import com.google.gson.Gson;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import javax.json.JsonValue;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DependencyRatioTest {

    List<String> parseJsonFile(String filepath) {
        try {
            Reader reader = Files.newBufferedReader(Paths.get(filepath));
            PackageJson packageJson = new Gson().fromJson(reader, PackageJson.class);
            return (List<String>) packageJson.dependencies;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyTestData.csv")
    void isMajMinPinned(String input, int expected) {
        DependencyRatio d = new DependencyRatio();
        assertEquals(d.isMajMinPinned(input), expected);
    }

    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyRatioData.csv")
    void getDependencyRatio(String filename, float expected) {
        String fullFile = "./package-test-files/" + filename + "-package.json";

        List<String> values = parseJsonFile(fullFile);
        DependencyRatio d = new DependencyRatio(values);
        float numDeps = d.getDependencyRatio();
//        Iterator<String> valIter = values.iterator();
//        String dependencyString = "";
//        while(valIter.hasNext()) {
//            String s = valIter.next();
//            dependencyString = dependencyString.concat(s.substring( 1, s.length() - 1 ));
//        }
        assertEquals(expected, numDeps);
    }

//    @ParameterizedTest
//    @CsvFileSource(resources = "/pinnedDependencyRatioData.csv")
//    void findNumPinnedDeps(String filename, float expected) {
////        DependencyRatio d = new DependencyRatio();
//        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
////        String package_json =
////        System.out.println("Working Directory = " + System.getProperty("user.dir"));
//
//        JsonReadHandler jHandler = new JsonReadHandler(fullFile);
//        Collection<String> values = jHandler.getFieldValues("dependencies");
//        int dependencies = 0;
//        dependencies = d.findNumPinnedDeps(values);
//        assertEquals(expected, dependencies);
//    }
//
//    @ParameterizedTest
//    @CsvFileSource(resources = "/totalDependencyRatioData.csv")
//    void findNumDeps() {
//        DependencyRatio d = new DependencyRatio(filename);
//        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
////        System.out.println("Working Directory = " + System.getProperty("user.dir"));
//        JsonHandler jHandler = new JsonHandler(fullFile);
//        Collection<JsonValue> values = jHandler.getFieldValues("dependencies");
//        int dependencies = 0;
//        dependencies = d.findNumPinnedDeps(values);
//        assertEquals(expected, dependencies);
//    }




//    void

}