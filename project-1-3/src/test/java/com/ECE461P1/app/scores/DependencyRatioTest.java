package com.ECE461P1.app.scores;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import javax.json.JsonValue;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.*;

class DependencyRatioTest {



    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyTestData.csv")
    void isMajMinPinned(String input, int expected) {
        DependencyRatio d = new DependencyRatio("");
        assertEquals(d.isMajMinPinned(input), expected);
    }

    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyRatioData.csv")
    void getDependencyRatio(String filename, float expected) {
        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
        DependencyRatio d = new DependencyRatio(filename);

//        System.out.println("Working Directory = " + System.getProperty("user.dir"));
//        JsonHandler jHandler = new JsonHandler(fullFile);
//        Collection<JsonValue> values = jHandler.getFieldValues("dependencies");
//        Iterator<JsonValue> valIter = values.iterator();
//        String dependencyString = "";
//        while(valIter.hasNext()) {
//            String s = valIter.next().toString();
//
//            dependencyString = dependencyString.concat(s.substring( 1, s.length() - 1 ));
//        }
        assertEquals(expected, d.getDependencyRatio());
    }

    @ParameterizedTest
    @CsvFileSource(resources = "/pinnedDependencyRatioData.csv")
    void findNumPinnedDeps(String filename, float expected) {
        DependencyRatio d = new DependencyRatio(filename);
        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
//        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        JsonReadHandler jHandler = new JsonReadHandler(fullFile);
        Collection<JsonValue> values = jHandler.getFieldValues("dependencies");
        int dependencies = 0;
        dependencies = d.findNumPinnedDeps(values);
        assertEquals(expected, dependencies);
    }
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