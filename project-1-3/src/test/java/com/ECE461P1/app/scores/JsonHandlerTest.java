package com.ECE461P1.app.scores;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonValue;

import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

class JsonHandlerTest {
    private JsonHandler jHandler;
    @BeforeEach
    void setUp() {
//        jHandler.parse("node_modules/chalk/package.json");
    }

    @AfterEach
    void tearDown() {
    }


    @ParameterizedTest
    @CsvFileSource(resources = "/testData.csv", numLinesToSkip = 0)
    void getField(String filename, String expected) {
        String fullFile = "node_modules/" + filename + "/package.json";
        jHandler = new JsonHandler(fullFile);
        Collection<JsonValue> values = jHandler.getFieldValues("dependencies");
        Iterator<JsonValue> valIter = values.iterator();
        String dependencyString = "";
        while(valIter.hasNext()) {
            String s = valIter.next().toString();
            dependencyString = dependencyString.concat(s.substring( 1, s.length() - 1 ));
        }

        assertEquals(expected, dependencyString);
    }

    @ParameterizedTest
    @CsvFileSource(resources = "/testDataError.csv", numLinesToSkip = 0)
    void getFieldFail(String filename, String expected) {
        String fullFile = "node_modules/" + filename + "/package.json";
        jHandler = new JsonHandler(fullFile);
        assertNull(jHandler.getFieldValues("dependencies"));
    }

    public JsonHandler jsonWrapper(String filename) {
        return new JsonHandler(filename);
    }

    @Test
    void invalidFileName() {

        assertDoesNotThrow(() -> {new JsonHandler("badfilename");});
        JsonHandler jHandler = new JsonHandler("badfilename");
        assertNotNull(jHandler);
        assertNull(jHandler.obj);
    }
//    @ParameterizedTest
//    @CsvFileSource(resources = "/data.csv", numLinesToSkip = 1)
//    void getFieldValue() {
//
//    }
}