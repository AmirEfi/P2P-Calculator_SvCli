import java.io.*;
import java.net.*;
import java.util.*;

public class Client {
    public Client(String address, int port)
    {
        try {
            Scanner sc = new Scanner(System.in);
            Socket s = new Socket(address, port);
            System.out.println("Connected!");

            DataInputStream dis = new DataInputStream(s.getInputStream());
            DataOutputStream dos = new DataOutputStream(s.getOutputStream());

            while (true) {
                System.out.println("Enter the operation in the form 'operator op1 op2' ('Over' for close connection): ");
                String inp = sc.nextLine();

                dos.writeUTF(inp);

                if (inp.equals("Over")) {
                    System.out.println("Connection closed.");
                    break;
                }

                String ans = dis.readUTF();
                StringTokenizer st = new StringTokenizer(ans);
                String time = st.nextToken();
                String result = st.nextToken();
                System.out.println("Calculation Time (in NanoSec) = " + time);
                System.out.println("Answer = " + result);
            }
        }
        catch (Exception e) {
            System.out.println("Error!");
        }
    }

    public static void main(String[] args) {
        Client client = new Client("127.0.0.1", 8080);
    }
}
