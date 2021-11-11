package com.ECE461P1.app.scores;

import javax.json.*;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

public class JsonWriteHandler {
    String filename;
    JsonArrayBuilder arrBuilder;
    JsonObjectBuilder jObject;
    public JsonWriteHandler(String _filename) {
        filename = _filename;
        arrBuilder = Json.createArrayBuilder();
        jObject = Json.createObjectBuilder();

    }
    public void addToArray(){
        arrBuilder.add(buildJsonObject());
    };
    private JsonArray buildArray() {
        JsonArray jArr = arrBuilder.build();
        arrBuilder = Json.createArrayBuilder();
        return jArr;
    }
    public void write(){
        try {
            Writer writer = new FileWriter(filename);
            JsonWriter jsonWriter = Json.createWriter(writer);
            jsonWriter.writeArray(buildArray());
            jsonWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void addUrlItem(String key, String val){
        jObject.add(key, val);
    }

    public void addUrlItem(String key, int val){
        jObject.add(key, val);
    }
    public void addUrlItem(String key, float val){
        jObject.add(key, val);
    }


    private JsonObject buildJsonObject() {
        JsonObject j = jObject.build();
        jObject = Json.createObjectBuilder();
        return j;
    }

}
