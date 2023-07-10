import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.Math;

public class Server {

    public Server(int port) {
        try {
            ServerSocket ss = new ServerSocket(port);
            System.out.println("Server started. Waiting for client request...");
            Socket s = ss.accept();
            System.out.println("Client connected!");

            DataInputStream dis = new DataInputStream(s.getInputStream());
            DataOutputStream dos = new DataOutputStream(s.getOutputStream());

            while (true) {
                String input = dis.readUTF();
                if (input.equals("Over")) {
                    System.out.println("Connection closed.");
                    break;
                }
                System.out.println("Equation received. Calculating...");
                double answer = 0;

                StringTokenizer st = new StringTokenizer(input);
                String operation = st.nextToken();
                double opd1 = Double.parseDouble(st.nextToken());
                double opd2 = 1;
                if (operation.length() == 1)
                    opd2 = Double.parseDouble(st.nextToken());

                long startTime = 0;
                long endTime = 0;

                switch (operation) {

                    case "+" -> {
                        startTime = System.nanoTime();
                        answer = opd1 + opd2;
                        endTime = System.nanoTime();
                    }
                    case "-" -> {
                        startTime = System.nanoTime();
                        answer = opd1 - opd2;
                        endTime = System.nanoTime();
                    }
                    case "/" -> {
                        startTime = System.nanoTime();
                        if (opd2 != 0)
                            answer = (double) opd1 / opd2;
                        endTime = System.nanoTime();
                    }
                    case "*" -> {
                        startTime = System.nanoTime();
                        answer = opd1 * opd2;
                        endTime = System.nanoTime();
                    }

                    case "sin" -> {
                        double op = Math.toRadians(opd1);
                        startTime = System.nanoTime();
                        answer = Math.sin(op);
                        endTime = System.nanoTime();
                    }
                    case "cos" -> {
                        double op = Math.toRadians(opd1);
                        startTime = System.nanoTime();
                        answer = Math.cos(op);
                        endTime = System.nanoTime();
                    }
                    case "tan" -> {
                        double op = Math.toRadians(opd1);
                        startTime = System.nanoTime();
                        answer = Math.tan(op);
                        endTime = System.nanoTime();
                    }
                    case "cot" -> {
                        double op = Math.toRadians(opd1);
                        startTime = System.nanoTime();
                        answer = 1 / Math.tan(op);
                        endTime = System.nanoTime();
                    }
                }
                long elapsedTime = endTime - startTime;
                String result = Double.toString(elapsedTime);
                result = result.concat(" " + answer);
                System.out.println("Sending the result...");
                dos.writeUTF(result);
            }
        }
        catch (Exception e) {
            System.out.println("Error!");
        }
    }

    public static void main(String[] args){
        Server server = new Server(8080);
    }
}
