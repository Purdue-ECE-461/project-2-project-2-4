package com.ECE461P1.app.scores;
import javax.json.Json;
import javax.json.JsonValue;
import java.util.Collection;
import java.util.regex.Pattern;
import java.util.Iterator;



public class DependencyRatio extends Score{
//    JsonHandler handler;
    String dirPath;
    public DependencyRatio(String _owner, String _repo) {
        super(_owner, _repo);
        dirPath = "";
    }
    public DependencyRatio(String _dirPath) {
        super();
        dirPath = _dirPath;
    }


    public void getDependencyRatio() {
        JsonHandler handler = new JsonHandler("./npmjs_repos/node_modules/" + repoName + "package.json");
        Collection<JsonValue> jsonVals = handler.getFieldValues("dependencies");
        try {
            jsonVals.size();
            score = (float) 1;
        } catch (Exception e) {
            score = (float) 0;
        }
    }

    int findNumPinnedDeps(Collection<JsonValue> jsonVals){
        if (jsonVals.size() == 0) return 1;
        int count = 0;
        Iterator<JsonValue> valIter = jsonVals.iterator();
        while(valIter.hasNext()){
            String s = valIter.next().toString();
            s = s.substring( 1, s.length() - 1 );
            System.out.println(s);
            count += isMajMinPinned(s);
        }

        return count;
    }

    int findNumDeps(Collection<JsonValue> jsonVals){
        if (jsonVals.size() == 0) return 1;
        return jsonVals.size();
    }

    public int isMajMinPinned(String s){
        s = cleanStr(s);
        if (isInvalidVersionStr(s))     return 0;
        if (isInvalidVersionRange(s))   return 0;
        if (isBadWildcard(s))           return 0;
        if (isNotVersion(s))            return 0;
        if (isBadCompare(s))            return 0;
        if (isBadCarrot(s))             return 0;
        if (isBadTilde(s))              return 0;

        logger.debug("{}", s);

        return 1;
    }
    public String cleanStr(String s) {
        s = s.toLowerCase();
        s = s.replaceAll("\\s+","");
        s = s.replaceAll("v","");
        return s;
    }

    public boolean isInvalidVersionStr(String s) {
        return s.equals((String) "");
    }

    public boolean isInvalidVersionRange(String s) {
        String regex = "([\\d]*)[.]([\\d]*)[.][[\\d]*|x]-([\\d]*)[.]([\\d]*)[.][[\\d]*|x]";
        if (Pattern.matches(regex, s)) {
            //regex for a valid version range... invert return condition for invalid
            regex = "([\\d]*)[.]([\\d]*)[.][\\d*|x]-(\\1)[.](\\2)[.][\\d*|x]";
            return !Pattern.matches(regex, s);
        }
        return false;
    }

    public boolean isBadWildcard(String s) {
        String regex = "((\\*)|([\\d]*[.][\\*|x]))[-]?[\\w|\\d]*";
        return (boolean) Pattern.matches(regex, s);
    }
    public boolean isBadCompare(String s) {
        String regex = ">=?.*";
        if (Pattern.matches(regex, s)) {
            return true;
        }

        regex = "<=?.*";
        if (Pattern.matches(regex, s)) {
            regex = "(<=?0.0.[\\d]*)|(<0.1.0)";

            if (!Pattern.matches(regex, s)) {
                return true;
            }
//            return true;
        }



        return false;
    }

    public boolean isNotVersion(String s) {
        String regex = "[\\d|\\w]*$";
        if (Pattern.matches(regex, s)) {
            return true;
        }
        return false;
    }

    public boolean isBadCarrot(String s) {
        //the 2 regex expressions are for all the valid carrot expressions,
        //if it doesn't match either then it's bad
        String regex = "\\^.*";
        if (Pattern.matches(regex, s)) {
            regex = "\\^[0]*[.][\\d]*[.][\\d]*.*";
            if (Pattern.matches(regex, s)) {
                return false;
            }
            regex = "\\^[1-9]*[.][1-9]*[.][\\d]*.*";
            if (Pattern.matches(regex, s)) {
                return false;
            }
            return true;
        }
        return false;
    }

    public boolean isBadTilde(String s) {

        String regex = "\\~.*";
        if (Pattern.matches(regex, s)) {
            regex = "~[\\d]*[.][\\d]*[.]*[\\d]*.*";
            return !Pattern.matches(regex, s);
        }
        return false;
    }
    //TODO: digits are not set up to handle repeating digits



}
