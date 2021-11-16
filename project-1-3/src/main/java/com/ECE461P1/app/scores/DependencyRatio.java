package com.ECE461P1.app.scores;
import java.io.FileReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.json.Json;
import javax.json.JsonReader;
import javax.json.JsonStructure;
import com.ECE461P1.app.scores.Score;
import org.apache.commons.io.IOUtils;



public class DependencyRatio extends Score{

    public DependencyRatio(String _owner, String _repo) {
        super(_owner, _repo);
    }

    public DependencyRatio() {
        super();
    }


    public void getDependencyRatio() {
        try {
            score = (float) 1;
        } catch (Exception e) {
            score = (float) 0;
        }
    }

    public int isMajMinPinned(String s){
        s = s.toLowerCase();
        if (!isValidVersionStr(s)) {
            return 0;
        }

//        s = s.split("[-]")[0];
//        String[] strSplit = s.split("[.]");
//        if (strSplit.length == 1) {
//            return 0;
//        }
        if (isValidVersionRange(s)) {
            return 1;
        }
        if (isBadWildcard(s)){
            return 0;
        }
        if (isNotVersion(s)){
            return 0;
        }
        if (isBadCompare(s)) {
            return 0;
        }

        logger.debug("{}", s);

//        switch(s.substring(0,1)) {
//            case ">": return 0;
//            case ""
//            default:
//                return 0;
//        }
        return 1;
    }
    public boolean isValidVersionStr(String s) {
        if (s.equals((String) "")) {
            return false;
        }
        return true;
    }

    public boolean isValidVersionRange(String s) {
        String regex = "[v]?([\\d])[.]([\\d])[.][\\d|x][\\s]?-[\\s]?[v]?(\\1)[.](\\2)[.][\\d|x]";
        return (boolean) Pattern.matches(regex, s);
    }

    public boolean isBadWildcard(String s) {
        String regex = "[v]?((\\*)|([\\d][.][\\*|x]))[-]?[\\w|\\d]*";
        return (boolean) Pattern.matches(regex, s);
    }
    public boolean isBadCompare(String s) {
        String regex = ">=?.*";
        if (Pattern.matches(regex, s)) {
            return true;
        }

        regex = "<=?.*";
        if (Pattern.matches(regex, s)) {
            regex = "(<=?0.0.[\\d])|(<0.1.0)";

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
    //TODO: digits are not set up to handle repeating digits
    final String regex = "[\\^]([1-9]*)[.]0[.]0";


}
