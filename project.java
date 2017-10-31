import java.time.LocalDateTime;

public class project{
   public static void main(String[] args){
      int packet;
      String status = "wait";
      String fileName = "Enter Address here";

      //open file

      while(1){
         //get packet value
         packet = 3; //temp

         if(packet == 0){ //loop
            status = "run";
            getData();
         } else if(packet == 1){ //kill
            status = "wait";
         } else if(packet == 2){ //sendFile
            //close file
            sendFile(fileName);
            //open file
         } else if(packet == 4){ //timeout
            if(status == "run"){
               getData();
            }
         }
      }
   }

   public static void getData(){
      int color;
      int data;

      //get data
      if(data < 5){
         color = 0; //red
      } else if (data < 10){
         color = 1; //yellow
      } else {
         color = 2; //green
      }
      //send color
      String stamped = addStamp(data);
      //save stamped

   }

   public static void sendFile(String fName){
      //send file
   }

   public static String addStamp(int d){
      String s = Integer.toString(d) + " - " + LocalDateTime.now();
      return s;
   }
}
