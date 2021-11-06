package com.ECE461P1.app.scores;
import java.io.FileReader;
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
        String exp = "";
        System.out.println(s);
        System.out.println(s.length());
        if (s == "a") {
            return 0;
        }
        return 1;
    }

}
