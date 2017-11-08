import java.time.LocalDateTime;
import java.io.*;
import java.net.*;

public class project{

   private static InetAddress clientIPAddress;
   private static int clientPort;
   private static byte[] recData;
   private static byte[] sendData;
   private static DatagramSocket sSock;

   public static void main(String[] args){

      /** set up UDP socket **/
      try{
         sSock = new DatagramSocket(8888); //new socket with port 8888
      } catch(Exception e){};
      recData = new byte[1024];
      sendData = new byte[1024]; //might need to change

      /** test values **/
      String status = "wait";
      String fileName = "Enter Address here";

      /** open file **/


      /** main loop **/
      while(true){
         //get packet value
         DatagramPacket recPacket = new DatagramPacket(recData, recData.length);
         try{
            sSock.receive(recPacket);
         } catch(Exception e){};
         String packet = new String(recPacket.getData());
         System.out.println("Packet is: " + packet);

         //get address and port of client
         clientIPAddress = recPacket.getAddress();
         clientPort = recPacket.getPort();

         //packet = 3; //temp

         if(packet == "loop"){ //loop
            status = "run";
            getData();
         } else if(packet == "kill"){ //kill
            status = "wait";
         } else if(packet == "sendFile"){ //sendFile
            //close file
            sendFile(fileName);
            //open file
         } else if(packet == "4"){ //timeout
            if(status == "run"){
               getData();
            }
         }
      }
   }

   private static void getData(){
      String color;
      int data = 0;

      //get data
      if(data < 5){
         color = "red"; //red
      } else if (data < 10){
         color = "yellow"; //yellow
      } else {
         color = "green"; //green
      }
      //send color
      sendData = color.getBytes();
      DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientIPAddress, clientPort);
      try{
         sSock.send(sendPacket);
      } catch(Exception e){};

      String stamped = addStamp(data);
      //save stamped

   }

   private static void sendFile(String fName){
      //send file
   }

   private static String addStamp(int d){
      String s = Integer.toString(d) + " - " + LocalDateTime.now();
      return s;
   }
}
