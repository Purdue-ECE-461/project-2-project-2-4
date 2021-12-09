package com.ECE461P1.app.scores;
import java.io.FileReader;
import javax.json.*;
import javax.json.JsonReader;
import javax.json.JsonValue;

import java.util.Collection;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static javax.json.JsonValue.ValueType.OBJECT;
import static javax.json.JsonValue.ValueType.STRING;

public class JsonReadHandler {
    static final Logger logger = LoggerFactory.getLogger(JsonReadHandler.class);

    JSONObject obj;


    public JsonReadHandler(JSONObject jsonObject){
//        logger.debug("New JsonHandler");
        obj = jsonObject;
//        JsonReader reader;
//        try {
//            reader = Json.createReader(new FileReader(filename));
//            obj = reader.readObject();
//            logger.debug("{}", obj);
//            reader.close();
//        }
//        catch (Exception e){
//            logger.debug("{}", e);
//            obj = null;
//        }
    }

    public Object getField(String fieldName){
        logger.debug("{}", obj.get(fieldName));
        return obj.get(fieldName);
    }

    public Collection<String> getFieldValues(String fieldName) {
        if (obj.optJSONArray(fieldName) == null) return null;
//        if (obj == null) return null;
        Collection<String> vals = null;
        JSONArray arr = obj.getJSONArray(fieldName);
        for (int i = 0; i < obj.getJSONArray(fieldName).length(); i++) {
            vals.add(arr.getString(i));
        }

        return vals;
    }

}
