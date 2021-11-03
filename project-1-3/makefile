include .env
export $(shell sed 's/=.*//' .env)

# sources
SRCSDIR := src/main/java/com/
SRCS := \
        App.java \
        testlog.java \
        com.ECE461P1.app.scores/Score.java \
        com.ECE461P1.app.scores/RampUpTime.java \
				com.ECE461P1.app.scores/Responsiveness.java \
				com.ECE461P1.app.scores/License.java \
				com.ECE461P1.app.scores/Correctness.java \
				com.ECE461P1.app.scores/BusFactor.java

# classes
CLSDIR := target/classes/java/com/
CLS := $(SRCS:%.java=%.class)

# compiler and compiler flags
JC := javac
JFLAGS := -g
# MVN := mvn
MVN := ./apache-maven-3.8.3/bin/mvn
MVNFLAGS := --log-file $(LOG_FILE)

.SUFFIXES: .java

$(CLSDIR)/$(CLS): all

jdb: $(CLSDIR)/$(CLS)
	jdb -classpath target/project-1-3-1.0-SNAPSHOT.jar com.ECE461P1.app.CommandExecutor express

run: $(CLSDIR)/$(CLS)
	java -cp target/project-1-3-1.0-SNAPSHOT.jar com.ECE461P1.app.App UrlFile.txt

all:
	$(MVN) $(MVNFLAGS) clean package shade:shade

clean:
	$(MVN) $(MVNFLAGS) clean
	rm -rf ./target
	rm -rf ./jacoco
	mkdir ./jacoco
	rm -f dependency-reduced-pom.xml

compile:
	$(MVN) $(MVNFLAGS) compile

test: $(CLSDIR)/$(CLS)
	$(MVN) $(MVNFLAGS) test

help:
	echo "Usage   :  make <target>"
	echo "Targets :"
	echo "   all ........... Builds the project"
	echo "   clean ......... Removes build products"
	echo "   compile ....... Compiles all Java files"
	echo "   test .......... Builds and runs all unit tests"
	echo "   help .......... Prints this help message"
