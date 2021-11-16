package com.ECE461P1.app.scores;
import java.util.Collection;
import java.util.regex.Pattern;
import java.util.Iterator;



public class DependencyRatio extends Score{
//    JsonHandler handler;
    String dirPath;
    Collection<String> versionList;
//    public DependencyRatio(String _owner, String _repo) {
//        super(_owner, _repo);
//        dirPath = "./src/test/resources/jsonTestFiles/" + repoName + "-package.json"; //TODO: replace with actual
//    }
    public DependencyRatio() { //testing purposes
        super();
//        repoName = _repoName;
//        dirPath = "./src/test/resources/jsonTestFiles/" + repoName + "-package.json";
    }
    public DependencyRatio(Collection<String> _versionList) {
        super();
        versionList = _versionList;
    }




    public float getDependencyRatio() {
//        JsonReadHandler handler = new JsonReadHandler(dirPath);
        try {
            float pinnedDeps = (float) findNumPinnedDeps(versionList);
            float numDeps = (float) findNumDeps(versionList);
            return (float) pinnedDeps / numDeps;
        } catch (Exception e) {
            return (float) 0;
        }
    }

    @Override
    public float getScore() {
        score = getDependencyRatio();
        return score;
    }


    int findNumPinnedDeps(Collection<String> versionList){
        if (versionList == null) return 1;
        if (versionList.size() == 0) return 1;
        int count = 0;
        Iterator<String> valIter = versionList.iterator();
        while(valIter.hasNext()){
            String s = valIter.next();
//            s = s.substring( 1, s.length() - 1 );
//            System.out.println(s);
            count += isMajMinPinned(s);
        }
//        System.out.println("pinned: " + count);
        return count;
    }

    int findNumDeps(Collection<String> jsonVals){
        if (jsonVals == null) return 1;
        if (jsonVals.size() == 0) return 1;
//        System.out.println("size" + jsonVals.size());

        return jsonVals.size();
    }

    public int isMajMinPinned(String s){
        s = cleanStr(s);
        if (isInvalidVersionStr(s))     return 0;
        if (isInvalidVersionRange(s))   return 0;
        if (isBadWildcard(s))           return 0;
        if (isNotVersion(s))            return 0;
        if (isBadCompare(s))            return 0;
        if (isBadCaret(s))              return 0;
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

            return !Pattern.matches(regex, s);
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

    public boolean isBadCaret(String s) {
        //the 2 regex expressions are for all the valid carrot expressions,
        //if it doesn't match either then it's bad
        String regex = "\\^.*";
        if (Pattern.matches(regex, s)) {
            regex = "\\^[0]*[.][\\d]*[.][\\d]*.*";
            if (Pattern.matches(regex, s)) {
                return false;
            }
//            regex = "\\^[1-9]*[.][1-9]*[.][\\d]*.*";
//            if (Pattern.matches(regex, s)) {
//                return false;
//            }
//            regex = "\\^[1-9]*[.][1-9]*[.][1-9]*.*";
//            if (Pattern.matches(regex, s)) {
//                return false;
//            }
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


}
