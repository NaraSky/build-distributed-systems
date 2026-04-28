// Website: https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-3-partition-leader
// Track 19: The Logger
// Task 18: Implement Partition Leader Election via Raft

// Java starter code
// Read from stdin, process data, write to stdout
// This is a general template - adapt it to your specific task

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

        try {
            String line;
            // Read input line by line
            while ((line = reader.readLine()) != null) {
                // TODO: Implement your task logic here
                // - Parse the input (might be JSON, plain text, etc.)
                // - Process according to the task requirements
                // - Output results to stdout

                // For debugging, use stderr:
                // System.err.println("Debug info: " + line);

                // Example: Echo input back (replace with your logic)
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading input: " + e.getMessage());
            System.exit(1);
        }
    }
}
