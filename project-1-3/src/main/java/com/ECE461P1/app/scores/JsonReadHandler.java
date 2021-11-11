package com.ECE461P1.app.scores;
import java.io.FileReader;
import javax.json.*;
import javax.json.JsonReader;
import javax.json.JsonValue;

import java.util.Collection;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static javax.json.JsonValue.ValueType.OBJECT;
import static javax.json.JsonValue.ValueType.STRING;

public class JsonReadHandler {
    static final Logger logger = LoggerFactory.getLogger(JsonReadHandler.class);

    JsonObject obj;


    public JsonReadHandler(String filename){
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
        if (obj == null) return null;
        JsonObject field = (JsonObject) obj.get(fieldName);
        logger.debug("getFieldValues returns: {}", field);
        if (field == null) {
            return null;
        }
        return field.values();
    }

    public String getURL() {
        JsonValue jGet = obj.get("repository");
        try {
            if (jGet.getValueType() == STRING) {
                System.out.println(jGet.toString());
                return jGet.toString();
            } else if (jGet.getValueType() == OBJECT) {
                JsonObject a = (JsonObject) jGet;
                String b = a.get("url").toString();
//                System.out.println(b);
                return b; //TODO: REGEX
                //TODO: 2 versions of package.json
            }
        }
        catch (Exception e) {
            System.out.println("Exception: " + e.toString());
        }
        return "";
    }
}
