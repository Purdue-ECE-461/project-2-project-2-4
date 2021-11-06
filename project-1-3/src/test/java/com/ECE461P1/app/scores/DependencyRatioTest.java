package com.ECE461P1.app.scores;
import com.ECE461P1.app.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import static org.junit.jupiter.api.Assertions.*;

class DependencyRatioTest {



    @ParameterizedTest
    @CsvFileSource(resources = "/dependencyTestData.csv", numLinesToSkip = 0)
    void isMajMinPinned(String input, int expected) { //TODO: why does this not work with csv
        DependencyRatio d = new DependencyRatio();
        String str = "a";
        System.out.println( str.strip() == input.strip());
        assertEquals(d.isMajMinPinned(input), expected);
    }

    @Test
    void isMajMinPinned1() {
        DependencyRatio d = new DependencyRatio();
        assertEquals(0, d.isMajMinPinned("a"));
    }
}