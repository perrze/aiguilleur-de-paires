import java.io.*;
import java.net.*;
import java.util.concurrent.TimeUnit;
public class androidSocket {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("10.0.0.5",13130);
            OutputStream os = socket.getOutputStream();
            InputStream isr = socket.getInputStream();
            os.write("a1b2c3e4f5a6".getBytes());
            os.flush();
            os.write("send e7d65a73a083 P4".getBytes());
            os.flush();
            byte[] buffer = new byte[1024];
            int len = isr.read(buffer);
            System.out.println("read");
            System.out.println(new String(buffer,0,len));
            TimeUnit.SECONDS.sleep(1);
            os.write("EXIT".getBytes());
            os.flush();
            os.close();
            socket.close();

        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }

    }
}

