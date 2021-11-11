package com.ECE461P1.app.scores;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonValue;
import javax.json.*;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.Collection;
import java.util.Iterator;
//import static javax.json.JsonObject.*
;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

class JsonHandlerTest {
    private JsonReadHandler jHandler;
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
        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
//        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        jHandler = new JsonReadHandler(fullFile);
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
    @CsvFileSource(resources = "/testData.csv", numLinesToSkip = 0)
    void getFieldUrl(String filename, String expected) {
        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
        JsonReadHandler jHandler = new JsonReadHandler(fullFile);
        System.out.println(jHandler.getURL());
    }

    @Test
    void testJsonOutput() {
//        String fullFile = "./src/test/resources/jsonTestFiles/" + filename + "-package.json";
//        System.out.println("Working Directory = " + System.getProperty("user.dir"));
//        jHandler = new JsonHandler("");
        JsonObject item = Json.createObjectBuilder()
                .add("url", "url.com")
                .add("busfactor", 1)
                .add("rampup", 2)
                .add("license", 3)
                .add("correctness", 4)
                .add("dependency", 5)
                .add("contributors", 6)
                .build();
        JsonObject item2 = Json.createObjectBuilder()
                .add("url", "url.com")
                .add("busfactor", 1)
                .add("rampup", 2)
                .add("license", 3)
                .add("correctness", 4)
                .add("dependency", 5)
                .add("contributors", 6)
                .build();
        JsonArray arr = Json.createArrayBuilder().add(item).add(item2).build();

        System.out.println(item.getInt("busfactor"));
        try {
            Writer writer = new FileWriter("output.json");
            JsonWriter jsonWriter = Json.createWriter(writer);
            jsonWriter.writeArray(arr);
            jsonWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        int i = 0;
        i = i + 1;

//        System.out.println(jHandler.obj.get("repository").getValueType() == STRING);

    }



    @ParameterizedTest
    @CsvFileSource(resources = "/testData.csv")
    void getFieldFail(String filename, String expected) {
        String fullFile = "node_modules/" + filename + "/package.json";
        jHandler = new JsonReadHandler(fullFile);
        assertNull(jHandler.getFieldValues("dependencies"));
    }

    public JsonReadHandler jsonWrapper(String filename) {
        return new JsonReadHandler(filename);
    }

    @Test
    void invalidFileName() {

        assertDoesNotThrow(() -> {new JsonReadHandler("badfilename");});
        JsonReadHandler jHandler = new JsonReadHandler("badfilename");
        assertNotNull(jHandler);
        assertNull(jHandler.obj);
    }
//    @ParameterizedTest
//    @CsvFileSource(resources = "/data.csv", numLinesToSkip = 1)
//    void getFieldValue() {
//
//    }
}