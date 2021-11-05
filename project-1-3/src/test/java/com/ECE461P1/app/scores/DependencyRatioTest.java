package com.ECE461P1.app.scores;
import com.ECE461P1.app.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DependencyRatioTest {

    @Test
    void makeHttpConnection() {
        Url url = new Url("https://github.com/jonschlinkert/even");
        DependencyRatio dependRatio = new DependencyRatio(url.ownerName, url.repoName);
        dependRatio.getDependencyRatio();
        assertEquals(dependRatio.score, 1);
    }

    @Test
    void getDependencyRatio() {
    }
}