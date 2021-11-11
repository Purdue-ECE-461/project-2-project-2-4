package com.ECE461P1.app.scores;
import com.ECE461P1.app.scores.*;

import org.junit.jupiter.api.Test;

import java.net.HttpURLConnection;

import static org.junit.jupiter.api.Assertions.*;

class ResponsivenessTest {

    @Test
    void getResponsivenessScore() {
        Responsiveness test = new Responsiveness("okmr-d", "DOFavoriteButton");
        System.out.println(test.getResponsivenessScore());

        HttpURLConnection conn = test.makeRespUrlConn("https://api.github.com/repos/chartjs/chartjs-plugin-datalabels/issues?state=closed");
        int i = 0;
        i++;
    }
}