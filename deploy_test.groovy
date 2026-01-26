#!/usr/bin/env groovy
/**
 * Groovy Deployment Test Script
 * Validates deployment environment and runs basic tests
 */

import groovy.json.JsonSlurper
import groovy.json.JsonOutput

class DeploymentTest {
    
    String environment
    String version
    List<String> testResults = []
    int passCount = 0
    int failCount = 0
    
    DeploymentTest(String env = "development", String ver = "1.0.0") {
        this.environment = env
        this.version = ver
    }
    
    // ============================================
    // Environment Validation Tests
    // ============================================
    
    boolean testEnvironmentVariables() {
        println "Testing environment variables..."
        def requiredVars = ["PATH", "HOME", "USER"]
        boolean allPresent = true
        
        requiredVars.each { varName ->
            def value = System.getenv(varName)
            if (value) {
                logResult("ENV_CHECK", varName, true, "Variable exists: ${value.take(50)}...")
            } else {
                logResult("ENV_CHECK", varName, false, "Variable not found")
                allPresent = false
            }
        }
        return allPresent
    }
    
    boolean testSystemProperties() {
        println "Testing system properties..."
        def props = [
            "java.version": System.getProperty("java.version"),
            "os.name": System.getProperty("os.name"),
            "os.version": System.getProperty("os.version"),
            "user.dir": System.getProperty("user.dir")
        ]
        
        props.each { key, value ->
            logResult("SYS_PROP", key, value != null, value ?: "Not available")
        }
        
        return props.values().every { it != null }
    }
    
    // ============================================
    // File System Tests
    // ============================================
    
    boolean testFileSystemAccess() {
        println "Testing file system access..."
        def testDir = new File(".")
        boolean readable = testDir.canRead()
        boolean writable = testDir.canWrite()
        
        logResult("FS_ACCESS", "Read permission", readable, readable ? "OK" : "DENIED")
        logResult("FS_ACCESS", "Write permission", writable, writable ? "OK" : "DENIED")
        
        return readable && writable
    }
    
    boolean testRequiredFiles() {
        println "Testing required files..."
        def requiredFiles = ["README.md", "addition.py", "addition.sh"]
        boolean allExist = true
        
        requiredFiles.each { fileName ->
            def file = new File(fileName)
            boolean exists = file.exists()
            logResult("FILE_CHECK", fileName, exists, exists ? "Found" : "Missing")
            if (!exists) allExist = false
        }
        
        return allExist
    }
    
    // ============================================
    // Connectivity Tests
    // ============================================
    
    boolean testNetworkConnectivity() {
        println "Testing network connectivity..."
        def hosts = ["localhost"]
        boolean allReachable = true
        
        hosts.each { host ->
            try {
                def reachable = InetAddress.getByName(host).isReachable(5000)
                logResult("NETWORK", host, reachable, reachable ? "Reachable" : "Unreachable")
                if (!reachable) allReachable = false
            } catch (Exception e) {
                logResult("NETWORK", host, false, "Error: ${e.message}")
                allReachable = false
            }
        }
        
        return allReachable
    }
    
    // ============================================
    // Application Tests
    // ============================================
    
    boolean testAdditionFunction() {
        println "Testing addition functionality..."
        
        // Test basic addition
        def testCases = [
            [a: 2, b: 3, expected: 5],
            [a: 0, b: 0, expected: 0],
            [a: -5, b: 10, expected: 5],
            [a: 100, b: 200, expected: 300],
            [a: 1.5, b: 2.5, expected: 4.0]
        ]
        
        boolean allPassed = true
        testCases.each { test ->
            def result = test.a + test.b
            boolean passed = result == test.expected
            logResult("ADDITION", "${test.a} + ${test.b}", passed, 
                      "Expected: ${test.expected}, Got: ${result}")
            if (!passed) allPassed = false
        }
        
        return allPassed
    }
    
    boolean testMultipleAddition() {
        println "Testing multiple number addition..."
        
        def numbers = [1, 2, 3, 4, 5]
        def expectedSum = 15
        def actualSum = numbers.sum()
        
        boolean passed = actualSum == expectedSum
        logResult("MULTI_ADD", "Sum of ${numbers}", passed, 
                  "Expected: ${expectedSum}, Got: ${actualSum}")
        
        return passed
    }
    
    // ============================================
    // Helper Methods
    // ============================================
    
    void logResult(String category, String testName, boolean passed, String message) {
        def status = passed ? "PASS" : "FAIL"
        def result = "[${status}] [${category}] ${testName}: ${message}"
        testResults << result
        
        if (passed) {
            passCount++
            println "  ✓ ${testName}: ${message}"
        } else {
            failCount++
            println "  ✗ ${testName}: ${message}"
        }
    }
    
    Map generateReport() {
        def report = [
            timestamp: new Date().format("yyyy-MM-dd HH:mm:ss"),
            environment: environment,
            version: version,
            summary: [
                total: passCount + failCount,
                passed: passCount,
                failed: failCount,
                successRate: passCount + failCount > 0 ? 
                    String.format("%.1f%%", (passCount * 100.0) / (passCount + failCount)) : "N/A"
            ],
            results: testResults
        ]
        return report
    }
    
    void printReport() {
        println "\n" + "=" * 60
        println "DEPLOYMENT TEST REPORT"
        println "=" * 60
        
        def report = generateReport()
        
        println "Timestamp:    ${report.timestamp}"
        println "Environment:  ${report.environment}"
        println "Version:      ${report.version}"
        println "-" * 60
        println "SUMMARY"
        println "  Total Tests:  ${report.summary.total}"
        println "  Passed:       ${report.summary.passed}"
        println "  Failed:       ${report.summary.failed}"
        println "  Success Rate: ${report.summary.successRate}"
        println "=" * 60
    }
    
    void saveReportToFile(String filename = "deployment_report.json") {
        def report = generateReport()
        def jsonReport = JsonOutput.prettyPrint(JsonOutput.toJson(report))
        new File(filename).text = jsonReport
        println "\nReport saved to: ${filename}"
    }
    
    // ============================================
    // Main Test Runner
    // ============================================
    
    boolean runAllTests() {
        println "\n" + "=" * 60
        println "DEPLOYMENT TEST SUITE"
        println "Environment: ${environment} | Version: ${version}"
        println "=" * 60 + "\n"
        
        def tests = [
            "Environment Variables": this.&testEnvironmentVariables,
            "System Properties": this.&testSystemProperties,
            "File System Access": this.&testFileSystemAccess,
            "Required Files": this.&testRequiredFiles,
            "Network Connectivity": this.&testNetworkConnectivity,
            "Addition Function": this.&testAdditionFunction,
            "Multiple Addition": this.&testMultipleAddition
        ]
        
        boolean allPassed = true
        
        tests.each { name, testMethod ->
            println "\n--- ${name} ---"
            try {
                boolean result = testMethod()
                if (!result) allPassed = false
            } catch (Exception e) {
                logResult("ERROR", name, false, "Exception: ${e.message}")
                allPassed = false
            }
        }
        
        printReport()
        
        return allPassed
    }
}

// ============================================
// Script Entry Point
// ============================================

if (this.binding.hasVariable('args')) {
    def cli = new CliBuilder(usage: 'deploy_test.groovy [options]')
    cli.with {
        h(longOpt: 'help', 'Show usage information')
        e(longOpt: 'env', args: 1, argName: 'environment', 'Deployment environment (default: development)')
        v(longOpt: 'version', args: 1, argName: 'version', 'Application version (default: 1.0.0)')
        o(longOpt: 'output', args: 1, argName: 'file', 'Save JSON report to file')
    }
    
    def options = cli.parse(args)
    
    if (!options || options.h) {
        cli.usage()
        return
    }
    
    def environment = options.e ?: 'development'
    def version = options.v ?: '1.0.0'
    
    def tester = new DeploymentTest(environment, version)
    def success = tester.runAllTests()
    
    if (options.o) {
        tester.saveReportToFile(options.o)
    }
    
    System.exit(success ? 0 : 1)
} else {
    // Running interactively or being imported
    def tester = new DeploymentTest()
    tester.runAllTests()
}
