package com.ECE461P1.app.scores;

import org.junit.jupiter.api.Test;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

import static org.junit.jupiter.api.Assertions.*;

class JsonWriteHandlerTest {

    @Test
    void write() {
        JsonWriteHandler jwHandler = new JsonWriteHandler("output.txt");

        jwHandler.addUrlItem("url", "url.com");
        jwHandler.addUrlItem("busfactor", 1);
        jwHandler.addToArray();
        jwHandler.addUrlItem("url", "url.com");
        jwHandler.addUrlItem("busfactor", 1);
        jwHandler.addToArray();
        jwHandler.write();

    }
}