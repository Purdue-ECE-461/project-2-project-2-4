package com.ECE461P1.app.scores;
import com.ECE461P1.app.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import static org.junit.jupiter.api.Assertions.*;

class DependencyRatioTest {



    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyTestData.csv")
    void isMajMinPinned(String input, int expected) {
        DependencyRatio d = new DependencyRatio("");
        assertEquals(d.isMajMinPinned(input), expected);
    }

}