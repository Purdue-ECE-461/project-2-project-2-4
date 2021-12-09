package com.ECE461P1.app.scores;
import java.io.FileReader;
import javax.json.*;
import javax.json.JsonObject.*;
import javax.json.JsonReader;
import javax.json.JsonValue;

import java.util.Collection;
import java.util.Iterator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JsonHandler {
    static final Logger logger = LoggerFactory.getLogger(JsonHandler.class);

    JsonObject obj;

    public JsonHandler(String filename){
        logger.debug("New JsonHandler");
        JsonReader reader;
        try {
            reader = Json.createReader(new FileReader(filename));
            obj = reader.readObject();
            logger.debug("{}", obj);
            reader.close();
        }
        catch (Exception e){
            logger.debug("{}", e);
            obj = null;
        }
    }

    public Object getField(String fieldName){
        logger.debug("{}", obj.get(fieldName));
        return obj.get(fieldName);
    }

    public Collection<javax.json.JsonValue> getFieldValues(String fieldName) {
        JsonObject field = (JsonObject) obj.get(fieldName);
        logger.debug("getFieldValues returns: {}", field);
        if (field == null) {
            return null;
        }
        return field.values();
    }

    public void parse(String fullFile) {
    }
}
