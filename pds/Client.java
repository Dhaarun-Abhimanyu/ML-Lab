import java.rmi.Naming;

public class Client {
   public static void main(String args[]) {
       try {
           Hello obj = (Hello) Naming.lookup("rmi://localhost/HelloService");
           String response = obj.sayHello();

           System.out.println(response);
       } catch ( Exception e){
           e.printStackTrace();
       }
   } 
}
