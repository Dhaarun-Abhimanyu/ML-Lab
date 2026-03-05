import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Server {
    public static void main(String args[]) {
        try {
            // Start RMI registry on port 1099 in the same JVM
            LocateRegistry.createRegistry(1099);

            HelloImpl obj = new HelloImpl();
            Naming.rebind("HelloService", obj);
            System.out.println("RMI Server is running...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}